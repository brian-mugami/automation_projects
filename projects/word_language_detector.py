import re
from collections import Counter
from random import sample

from docx import Document
from langdetect import detect, LangDetectException

from projects.utils import LANGUAGE_CODES


def detect_word_language(doc: str, sample_size=500):
    detected_languages = Counter()
    try:
        doc = Document(doc)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        sentences = []
        for paragraph in paragraphs:
            sentences.extend(re.split(r'(?<=[.!?]) +', paragraph))
        sampled_sentences = sample(sentences, min(len(sentences), sample_size))
        for sentence in sampled_sentences:
            try:
                language = detect(sentence)
                detected_languages[language] += 1
            except LangDetectException:
                continue
        most_common_language = detected_languages.most_common(1)
        if most_common_language:
            dominant_language_code = most_common_language[0][0]
            dominant_language = LANGUAGE_CODES.get(dominant_language_code, dominant_language_code)
        else:
            dominant_language = "Unknown"
        return dominant_language, detected_languages
    except Exception as e:
        print(f"Error processing the document: {e}")
        return "Unknown", Counter()
