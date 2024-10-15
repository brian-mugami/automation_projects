from PyPDF2 import PdfReader, PdfWriter


def remove_blank_pages(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Iterate through each page in the PDF
    for page in reader.pages:
        # Extract text from the page
        text = page.extract_text()

        # Check if the page is blank (no text)
        if text.strip():  # If there is text, keep the page
            writer.add_page(page)

    # Write the output PDF
    with open(output_pdf, 'wb') as f:
        writer.write(f)

    print(f"Blank pages removed. New PDF saved as: {output_pdf}")

# Example usage
# input_pdf = 'output_document.pdf'  # Replace with your input PDF file
# output_pdf = 'output_document_no_blanks.pdf'  # Output PDF file without blank pages
# remove_blank_pages(input_pdf, output_pdf)
