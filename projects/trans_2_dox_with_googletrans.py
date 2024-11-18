import time

from docx import Document
from googletrans import Translator


def translate_text_individually(doc_path: str, target: str = "fr", retries: int = 5, max_chunk_size=500):
    """
    Translates text in a Word document while preserving formatting and retrying failed attempts.
    """
    doc = Document(doc_path)
    translator = Translator()
    print("Translation started...")

    elements_translated = 0
    total_elements = sum(1 for _ in iterate_text_elements(doc))
    if total_elements == 0:
        print("No translatable text found.")
        return

    print(f"Found {total_elements} elements to translate.")

    for element_type, element in iterate_text_elements(doc):
        original_text = clean_text(''.join(run.text for run in element.runs if run.text).strip())
        if not original_text:
            continue  # Skip empty text

        # Retry mechanism for each element
        translated_text = retry_individual_translation(translator, original_text, target, retries, max_chunk_size)
        if translated_text and len(translated_text.split()) >= 0.8 * len(original_text.split()):
            apply_translated_text_to_runs(element, translated_text)
        else:
            print(f"Warning: Translation failed or incomplete for element: {original_text[:50]}...")

        elements_translated += 1
        print_progress(elements_translated, total_elements)

    print("Translation completed.")
    doc.save("translated_document_200.docx")


def iterate_text_elements(doc):
    """Generator to iterate over all paragraphs and table cells in a Word document."""
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            yield ('paragraph', paragraph)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if paragraph.text.strip():
                        yield ('cell', paragraph)


def retry_individual_translation(translator, text, target, retries=5, delay=2, max_chunk_size=500):
    """Attempts to translate a single text with retries and splits large text into chunks."""
    translated_chunks = []
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    for chunk in chunks:
        for attempt in range(retries):
            try:
                translated_chunks.append(translator.translate(chunk, dest=target).text)
                break  # Exit retry loop for this chunk on success
            except Exception as e:
                print(f"Error translating text chunk on attempt {attempt + 1}: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)  # Wait before retrying
                else:
                    print(f"Failed to translate chunk: {chunk[:50]}...")  # Log the failed chunk

    return ' '.join(translated_chunks)


def apply_translated_text_to_runs(paragraph, translated_text):
    """Applies translated text to a paragraph while preserving original run styles."""
    translated_words = translated_text.split()
    current_word_index = 0

    for run in paragraph.runs:
        if run.text:
            run_text_words = run.text.split()
            words_to_take = translated_words[current_word_index:current_word_index + len(run_text_words)]
            run.text = ' '.join(words_to_take)
            current_word_index += len(words_to_take)


def clean_text(text):
    """Cleans text to handle special characters or formatting issues."""
    return text.replace('\xa0', ' ').strip()  # Replace non-breaking spaces with regular spaces


def print_progress(completed, total):
    """Prints translation progress incrementally."""
    print(f"Translation progress: {completed}/{total} completed ({(completed / total) * 100:.2f}%)")


