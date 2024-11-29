import logging
import re

import pdfplumber
from pypdf import PdfReader, PdfWriter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MpesaStatementException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def extract_details(detail):
    detail = detail.strip().replace("\n", " ")
    match = re.search(r'-(.*)', detail)
    if match:
        return match.group(1).strip()
    return detail.strip()


def read_mpesa_pdf(pdf_path: str, decrypted_pdf_path="decrypted_pdf.pdf", pdf_password=None):
    try:
        pdf_reader = PdfReader(pdf_path)
        status = ""
        transactions = []
        if pdf_reader.is_encrypted:
            if not pdf_password:
                raise MpesaStatementException("PDF is encrypted, but no password was provided.")
            pdf_reader.decrypt(pdf_password)
            status = "PDF decrypted successfully."
            if decrypted_pdf_path:
                pdf_writer = PdfWriter()
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
                with open(decrypted_pdf_path, "wb") as f:
                    pdf_writer.write(f)
                pdf_to_read = decrypted_pdf_path
            else:
                logger.info("Decrypted PDF path not provided; using in-memory decryption.")
                pdf_to_read = pdf_path
        else:
            logger.info("This PDF is not encrypted.")
            pdf_to_read = pdf_path

        logger.info("Extracting tables with PDFPlumber:")
        with pdfplumber.open(pdf_to_read) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                # logger.info(f"Processing page {page_num}...")
                tables = page.extract_tables()
                for table_num, table in enumerate(tables, start=1):
                    # logger.info(f"Processing table {table_num} on page {page_num}...")
                    headers = table[0]
                    for row_idx, row in enumerate(table[1:], start=1):
                        transaction = {
                            headers[col]: extract_details(cell) if headers[col] == "Details" else cell
                            for col, cell in enumerate(row)
                        }
                        transaction['Page Number'] = page_num
                        transaction['Table Number'] = table_num
                        transactions.append(transaction)
        transactions.append({"status": status})
        return transactions
    except Exception as e:
        logger.error(f"MpesaStatementException: {e}")
        raise MpesaStatementException(f"An error occurred:{e}")

# results = read_mpesa_pdf("MPESA_Statement_2024-05-11_to_2024-11-11_2547xxxxxx200.pdf", pdf_password="719794")

# for result in results:
#    print(f"{result}\n")
