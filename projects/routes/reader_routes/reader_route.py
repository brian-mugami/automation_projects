import os

from flask import Blueprint, render_template, request, current_app, send_file, flash
from werkzeug.utils import secure_filename

from .reader_forms import PDFForm
from ...side_proj import get_tables, GetTableException
from ...side_proj_4 import extract_tables_from_pdf, create_excel_with_tables, TableException
from ...side_proj_8 import remove_blank_pages,remove_blank_docx

reader_blp = Blueprint("reader_blp", __name__)
PAGE_ERROR = "The from page number must be lesser then the to page number"
TABLE_ERROR = "No tables in the found in the pages given"
NOT_PDF = "This file is not a pdf"


@reader_blp.route("/read-home")
def reader_main_page():
    return render_template('reader_templates/reader_home.html')


@reader_blp.route("/remove-word", methods=["POST", "GET"])
def remove_word_pages():
    form = PDFForm()
    file = form.word_file.data
    if request.method == "POST":
        if file.content_type not in ["application/msword",
                                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            flash("Uploaded file is not a Word document.", category="error")
        else:
            try:
                filename = secure_filename(file.filename)
                name = file.filename.split(".")
                upload_dir = os.path.join(current_app.root_path, "static", "files")
                word_dir = os.path.join(current_app.root_path, "static", "word_files")
                os.makedirs(upload_dir, exist_ok=True)
                os.makedirs(word_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)
                word_path = os.path.join(word_dir, f"{name}.doc")
                file.save(file_path)
                remove_blank_docx(file_path,word_path)
                if os.path.exists(word_path):
                    print("Word file exists:", word_path)
                    return send_file(word_path, as_attachment=True, download_name=f"{name}.doc")
                else:
                    print("Word file does not exist:", word_path)
                    flash("Failed to create Word file.", category="error")
            except Exception as e:
                print(str(e))
                flash("An error occurred!!", category="error")
    return render_template('reader_templates/remove_word.html', form=form)


@reader_blp.route("/remove", methods=["POST", "GET"])
def remove_pages():
    form = PDFForm()
    file = form.file.data
    if request.method == "POST":
        if file.content_type != "application/pdf":
            flash(NOT_PDF, category="error")
        else:
            try:
                filename = secure_filename(file.filename)
                name = file.filename.split(".")
                upload_dir = os.path.join(current_app.root_path, "static", "files")
                pdf_dir = os.path.join(current_app.root_path, "static", "pdf_files")
                os.makedirs(upload_dir, exist_ok=True)
                os.makedirs(pdf_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)
                pdf_path = os.path.join(pdf_dir, f"{name}.pdf")
                file.save(file_path)
                remove_blank_pages(file_path, pdf_path)
                if os.path.exists(pdf_path):
                    print("PDF file exists:", pdf_path)
                    return send_file(pdf_path, as_attachment=True, download_name=f"{name}.pdf")
                else:
                    print("PDF file does not exist:", pdf_path)
                    flash("Failed to create PDF file.", category="error")
            except Exception as e:
                print(str(e))
                flash("An error occurred!!", category="error")
    return render_template('reader_templates/remove_pdf.html', form=form)


@reader_blp.route("/read-whole", methods=["POST", "GET"])
def reader_page():
    form = PDFForm()
    file = form.file.data
    to_page = form.to_page.data
    from_page = form.from_page.data

    if request.method == "POST":
        if file.content_type != "application/pdf":
            flash(NOT_PDF, category="error")
        elif to_page and from_page and to_page <= from_page:
            flash(PAGE_ERROR, category="error")
        else:
            try:
                filename = secure_filename(file.filename)
                name = file.filename.split(".")
                upload_dir = os.path.join(current_app.root_path, "static", "files")
                excel_dir = os.path.join(current_app.root_path, "static", "excel_files")
                os.makedirs(upload_dir, exist_ok=True)
                os.makedirs(excel_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                tables = extract_tables_from_pdf(file_path, to_page=to_page, from_page=from_page)
                excel_path = os.path.join(excel_dir, f"{name[0]}.xlsx")
                create_excel_with_tables(tables, excel_path)
                if os.path.exists(excel_path):
                    print("Excel file exists:", excel_path)
                else:
                    print("Excel file does not exist:", excel_path)
                    flash("Failed to create Excel file.", category="error")
                return send_file(excel_path, as_attachment=True, download_name=f"{name[0]}.xlsx")
            except TableException as e:
                flash(TABLE_ERROR, category="error")

    return render_template('reader_templates/reader_pdf.html', form=form)


@reader_blp.route("/read", methods=["POST", "GET"])
def reader_homepage():
    form = PDFForm()
    file = form.file.data
    if request.method == "POST":

        if file.content_type != "application/pdf":
            print(f"Uploaded File Name: {file.filename}")
            print(f"Uploaded File Content Type: {file.content_type}")
            return "This file is not a pdf"
        else:
            try:
                print(f"Uploaded File Name: {file.filename}")
                print(f"Uploaded File Content Type: {file.content_type}")
                filename = secure_filename(file.filename)
                name = file.filename.split(".")
                print(name[0])
                upload_dir = os.path.join(current_app.root_path, "static", "files")
                csv_path = os.path.join(current_app.root_path, "static", "csv_files")
                excel_path = os.path.join(current_app.root_path, "static", "excel_files")
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)

                file.save(file_path)

                excel_file_path = get_tables(file_path, str(form.page.data), name=name[0], csv_path=csv_path,
                                             excel_path=excel_path)
                if os.path.exists(excel_file_path):
                    print("Excel file exists:", excel_file_path)
                else:
                    print("Excel file does not exist:", excel_file_path)
                print("Excel file path:", excel_file_path)
                return send_file(excel_file_path, as_attachment=True, download_name=f"{name[0]}.xlsx")
            except GetTableException as e:
                flash(TABLE_ERROR, category="error")
            except Exception as e:
                print(e)
                flash(TABLE_ERROR, category="error")
    return render_template('reader_templates/reader.html', form=form)
