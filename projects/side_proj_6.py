from io import BytesIO

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_page_number_overlay(number, width, height, x, y):
    """
    Create a PDF overlay with the page number at specified (x, y) coordinates.
    """
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    # Draw the page number at the specified coordinates
    can.drawString(x, y, str(number))
    can.save()

    # Move to the beginning of the BytesIO buffer
    packet.seek(0)
    return PdfReader(packet)


def paginate_pdf(input_pdf_path, output_pdf_path, start_num=1, end_num=None, x_offset=50, y_offset=20):
    # Read the input PDF
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)

    # If end_num is None, assume the numbering should continue to the last page
    if end_num is None:
        end_num = total_pages + (start_num - 1)

    # Create a PDF writer object for the output file
    writer = PdfWriter()

    # Loop through each page of the input PDF
    for page_num in range(total_pages):
        page = reader.pages[page_num]

        # Add pagination only if we are within the range of total pages
        if start_num <= end_num:
            # Get the size of the current page
            width, height = page.mediabox.upper_right

            # Create a new page with the page number at specified coordinates
            overlay_pdf = create_page_number_overlay(start_num, width, height, width - x_offset, y_offset)

            # Merge the page number onto the original PDF page
            page.merge_page(overlay_pdf.pages[0])

            # Increment the start number for the next page
            start_num += 1

        # Add the (possibly) modified page to the writer
        writer.add_page(page)

    # If start_num is still less than end_num, create blank pages with pagination until the end_num
    while start_num <= end_num:
        # Create a blank page with the desired size (letter size by default)
        blank_page = BytesIO()
        can = canvas.Canvas(blank_page, pagesize=letter)
        width, height = letter
        # Add the page number to the blank page at specified coordinates
        can.drawString(width - x_offset, y_offset, str(start_num))
        can.showPage()
        can.save()

        # Convert the blank page into a PDF page and add it to the writer
        blank_page.seek(0)
        overlay_pdf = PdfReader(blank_page)
        writer.add_page(overlay_pdf.pages[0])

        # Increment the start number
        start_num += 1

    # Write the final output to the file
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)

    print(f"Pagination completed. Output saved at {output_pdf_path}.")

# Example usage:
# paginate_pdf("input.pdf", "output.pdf", start_num=1, end_num=10, x_offset=50, y_offset=20)
# paginate_pdf("database19c-wp_pdf_paginated_from_1_1_initialized_with_TRM.pdf", "output.pdf", start_num=50, x_offset=300, y_offset=20)
