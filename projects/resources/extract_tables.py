import camelot
import pandas as pd


class GetTableException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def get_tables(path: str, page: str, csv_path: str, excel_path: str, name: str) -> str:
    table_list = camelot.read_pdf(path, pages=page)
    if table_list == 0:
        raise GetTableException("No tables in the list")
    else:
        csv_file_path = f"{csv_path}/{name}.csv"
        table_list.export(csv_file_path, f="csv", compress=True)
        df2 = pd.concat([table.df for table in table_list])
        excel_file_path2 = f"{excel_path}/{name}.xlsx"
        df2.to_excel(excel_file_path2, index=False, engine='openpyxl')
        return excel_file_path2
