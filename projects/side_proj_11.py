from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_page_number_overlay(number_str, width, height, x, y):
    """
    Create a PDF overlay with the page number at specified (x, y) coordinates, keeping leading zeros.

    :param number_str: The page number to be displayed (as a string, preserving leading zeros).
    :param width: The width of the page.
    :param height: The height of the page.
    :param x: The x-coordinate to place the page number.
    :param y: The y-coordinate to place the page number.
    :return: A PdfReader object containing the overlay page.
    """
    # Create a new PDF page in memory (overlay)
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))

    # Draw the page number at the specified coordinates
    can.drawString(x, y, number_str)
    can.save()

    # Move to the beginning of the BytesIO buffer and return it as a PdfReader object
    packet.seek(0)
    return PdfReader(packet)


def paginate_pdf(input_pdf_path, output_pdf_path, start_num_str, end_num=None, x_offset=50, y_offset=20):
    """
    Paginate the given PDF by adding page numbers starting from 'start_num_str', with leading zeros preserved.

    :param input_pdf_path: The path to the input PDF file.
    :param output_pdf_path: The path to save the paginated output PDF file.
    :param start_num_str: The starting page number as a string (e.g., "001" or "000001").
    :param end_num: The ending page number (if None, paginate until the last page).
    :param x_offset: The x-coordinate offset for the page number's position.
    :param y_offset: The y-coordinate offset for the page number's position.
    """
    # Get the total length of the initial start number string (e.g., "001" has length 3)
    num_length = len(start_num_str)

    # Convert the input start number string to an integer for arithmetic, but store the string for formatting
    start_num = int(start_num_str)

    # Read the input PDF
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)

    # If end_num is None, continue numbering until the last page of the PDF
    if end_num is None:
        end_num = total_pages + (start_num - 1)

    # Create a PDF writer object for the output PDF
    writer = PdfWriter()

    # Loop through each page of the input PDF
    for page_num in range(total_pages):
        page = reader.pages[page_num]

        # Add pagination if we're still within the range of total pages
        if start_num <= end_num:
            # Get the size of the current page (width and height)
            width, height = page.mediabox.upper_right

            # Convert the current start_num back to a zero-padded string
            page_number_str = str(start_num).zfill(num_length)

            # Create a page overlay with the page number and merge it with the original page
            overlay_pdf = create_page_number_overlay(page_number_str, width, height, width - x_offset, y_offset)
            page.merge_page(overlay_pdf.pages[0])

            # Increment the page number for the next page
            start_num += 1

        # Add the modified page to the writer
        writer.add_page(page)

    # If start_num is still less than end_num, create blank pages with pagination until the end_num is reached
    while start_num <= end_num:
        # Create a blank page (letter size by default)
        blank_page = BytesIO()
        can = canvas.Canvas(blank_page, pagesize=letter)
        width, height = letter

        # Convert the current start_num back to a zero-padded string
        page_number_str = str(start_num).zfill(num_length)

        # Add the page number to the blank page at the specified coordinates
        can.drawString(width - x_offset, y_offset, page_number_str)
        can.showPage()
        can.save()

        # Convert the blank page into a PDF page and add it to the writer
        blank_page.seek(0)
        overlay_pdf = PdfReader(blank_page)
        writer.add_page(overlay_pdf.pages[0])

        # Increment the start number for the next blank page
        start_num += 1

    # Write the final output PDF to the file
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)

    print(f"Pagination completed. Output saved at {output_pdf_path}.")
