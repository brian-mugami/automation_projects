import camelot


def get_tables(path: str, page: str, name: str):
    tables = camelot.read_pdf(path, pages=page)
    tables.export(f"{name}.csv", f="csv", compress=True)
