import camelot
from pypdf import PdfReader, PdfWriter

encrypted_pdf_path = "MPESA_Statement_2024-05-11_to_2024-11-11_2547xxxxxx200 (1).pdf"
decrypted_pdf_path = "decrypted_file.pdf"
password = "719794"

pdf_reader = PdfReader(encrypted_pdf_path)
if pdf_reader.is_encrypted:
    try:
        if pdf_reader.decrypt(password):
            print("PDF decrypted successfully.")
            pdf_writer = PdfWriter()
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            with open(decrypted_pdf_path, "wb") as f:
                pdf_writer.write(f)
            print("Extracting tables with Tabula:")
            tables_tabula = camelot.read_pdf(decrypted_pdf_path, pages="all", multiple_tables=True)
            for i, table in enumerate(tables_tabula):
                print(f"Table {i + 1} with Tabula:")
                print(table)
        else:
            print("Incorrect password. Unable to decrypt the PDF.")
    except Exception as e:
        print("An error occurred while decrypting the PDF:", e)
else:
    print("This PDF is not encrypted.")
