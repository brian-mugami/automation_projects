from io import BytesIO

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def add_image_to_pdf(input_pdf_path, output_pdf_path, image_path, img_width=30, img_height=30, x_axis=0, y_axis=0):
    # Read the original PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Loop through all the pages of the PDF
    for page_num in range(len(reader.pages)):
        # Get the page
        page = reader.pages[page_num]

        # Create a canvas using reportlab on an in-memory buffer
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        # Insert image at the specified location (x_axis, y_axis)
        can.drawImage(ImageReader(image_path), x_axis, y_axis, width=img_width, height=img_height)

        # Finalize the canvas and move to the buffer
        can.save()

        # Move the buffer's cursor to the beginning
        packet.seek(0)

        # Merge the canvas with the original page
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])

        # Add the page to the writer
        writer.add_page(page)

    # Write the output to a new PDF
    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)


def add_word_to_pdf(input_pdf_path, output_pdf_path, word, font="Helvetica", font_size=10, x_axis=0, y_axis=0):
    # Read the original PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        # Get the page
        page = reader.pages[page_num]

        # Create a canvas using reportlab on an in-memory buffer
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        # Set the font size
        can.setFont(font, font_size)
        # Define coordinates (bottom left) for the word
        # (0, 0) is the bottom left corner; adjust y-position if needed
        can.drawString(x_axis, y_axis, word)

        # Finalize the canvas and move to the buffer
        can.save()

        # Move the buffer's cursor to the beginning
        packet.seek(0)

        # Merge the canvas with the original page
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])

        # Add the page to the writer
        writer.add_page(page)

    # Write the output to a new PDF
    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)

