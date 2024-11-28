from pdf2docx import Converter


def convert_pdf_to_word(pdf_file_path, word_file_path):
    cv = Converter(pdf_file_path)

    cv.convert(word_file_path, start=0, end=None)

    cv.close()
    print(f"Converted PDF to Word: {word_file_path}")
