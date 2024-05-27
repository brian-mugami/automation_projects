import os

import pandas as pd
import pdfplumber
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook

NO_TABLES = "No tables in the range riven"


class TableException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def extract_tables_from_pdf(pdf_path, from_page: int = None, to_page: int = None):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if from_page is not None and i + 1 < from_page:
                continue
            if to_page is not None and i + 1 > to_page:
                break
            page_tables = page.extract_tables()
            for table in page_tables:
                tables.append(table)
    if len(tables) == 0:
        raise TableException(NO_TABLES)
    return tables


def create_excel_with_tables(tables, excel_path):
    if not os.path.exists(excel_path):
        wb = Workbook()
        wb.save(excel_path)
    sheet_counter = 1
    for table in tables:
        df = pd.DataFrame(table[1:], columns=table[0])
        sheet_name = f"Sheet_{sheet_counter}"
        while sheet_name in load_workbook(excel_path).sheetnames:
            sheet_counter += 1
            sheet_name = f"Sheet_{sheet_counter}"
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        sheet_counter += 1
