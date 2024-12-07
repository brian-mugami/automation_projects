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
        transactions = []

        if pdf_reader.is_encrypted:
            if not pdf_password:
                raise MpesaStatementException("PDF is encrypted, but no password was provided.")
            if pdf_reader.decrypt(pdf_password):
                status = "PDF decrypted successfully."
                logger.info(status)
            else:
                raise MpesaStatementException("Failed to decrypt the PDF. Invalid password.")
            if decrypted_pdf_path:
                pdf_writer = PdfWriter()
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
                with open(decrypted_pdf_path, "wb") as f:
                    pdf_writer.write(f)
                pdf_to_read = decrypted_pdf_path
            else:
                pdf_to_read = pdf_path
        else:
            logger.info("This PDF is not encrypted.")
            pdf_to_read = pdf_path
            status = "PDF was not encrypted."

        logger.info("Extracting tables with PDFPlumber:")
        with pdfplumber.open(pdf_to_read) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                for table_num, table in enumerate(tables, start=1):
                    headers = table[0]  # Assuming the first row contains headers
                    for row_idx, row in enumerate(table[1:], start=1):
                        if len(headers) != len(row):
                            logger.warning(f"Header-row mismatch on page {page_num}, table {table_num}, row {row_idx}")
                            continue
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
        logger.error(f"An error occurred while reading the PDF: {e}")
        raise MpesaStatementException(f"An error occurred: {e}")


# results = read_mpesa_pdf("Statement.pdf")
#
# for result in results:
#     print(f"{result}\n")