import logging
import re

import camelot
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


def read_mpesa_pdf(pdf_path: str, decrypted_pdf_path=None, pdf_password=None):
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

        logger.info("Extracting tables with Camelot:")
        tables = camelot.read_pdf(pdf_to_read, pages="all", multiple_tables=True)
        for table_num, table in enumerate(tables, start=1):
            # logger.info(f"\nProcessing Table {table_num}...")
            raw_header = table.df.iloc[0, 0]
            headers = [header.strip() for header in raw_header.split("\n")]
            for row_idx, row in table.df.iterrows():
                if row_idx == 0:
                    continue
                transaction = {
                    headers[col]: extract_details(row[col]) if headers[col] == "Details" else row[col]
                    for col in range(len(headers))
                }
                transaction['Table Number'] = table_num
                transactions.append(transaction)
        transactions.append({"status": status})
        return transactions
    except Exception as e:
        logger.error(f"MpesaStatementException: {e}")
        raise MpesaStatementException(f"An error occurred:{e}")
