import re

import fitz
from googletrans import Translator
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

from projects.utils import LANGUAGE_CODES

DetectorFactory.seed = 0


def detect_languages(pdf_path):
    unique_languages = set()
    text_content = ""

    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            page_text = page.get_text("text")
            text_content += page_text

            # Split text into sentences based on punctuation
            sentences = re.split(r'(?<=[.!?]) +', page_text)

            # Limit to first few sentences if there's a lot of text
            for sentence in sentences[:10]:  # Check only first few sentences to diversify
                try:
                    if sentence.strip():  # Ensure there's content to detect
                        language = detect(sentence)
                        unique_languages.add(language)
                except LangDetectException:
                    continue

            if len(unique_languages) < 2:
                words = page_text.split()
                for word in words[:50]:
                    try:
                        if word.strip():
                            language = detect(word)
                            unique_languages.add(language)
                    except LangDetectException:
                        continue

    language_list = [LANGUAGE_CODES.get(code, code) for code in unique_languages]
    print(f"Detected Languages: {language_list}")

    return language_list, text_content

