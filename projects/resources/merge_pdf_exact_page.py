from typing import List

import PyPDF2


class PDFMergeException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def merge_multiple_pdfs(main_pdf_path: str, output_path: str, pdfs_to_merge: List):
    try:
        main_reader = PyPDF2.PdfReader(main_pdf_path)
        pdf_writer = PyPDF2.PdfWriter()
        pages_processed = 0
        for pdf_path, insert_at in sorted(pdfs_to_merge, key=lambda x: x[1]):
            if insert_at < 1 or insert_at > len(main_reader.pages) + 1:
                raise PDFMergeException(f"Insertion point for {pdf_path} is out of range!")
            for i in range(pages_processed, insert_at - 1):
                pdf_writer.add_page(main_reader.pages[i])
            pdf_to_insert_reader = PyPDF2.PdfReader(pdf_path)
            for page in pdf_to_insert_reader.pages:
                pdf_writer.add_page(page)

            pages_processed = insert_at - 1
        for i in range(pages_processed, len(main_reader.pages)):
            pdf_writer.add_page(main_reader.pages[i])
        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)
    except Exception as e:
        raise PDFMergeException(f"An error occurred while merging PDFs: {e}")



