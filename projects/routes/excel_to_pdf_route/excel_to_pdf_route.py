import os

from flask import Blueprint, request, flash, current_app, send_file, render_template
from werkzeug.utils import secure_filename

from .excel_to_pdf_form import ExcelForm
from ...side_proj_10 import convert_excel_to_pdf
from ...side_proj_12 import convert_excel_to_word
from ...side_proj_13 import convert_pdf_to_word
excel_blp = Blueprint("excel_blp", __name__)
NOT_EXCEL = "This file is not an excel"
content_type = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel", ]


@excel_blp.route("/excel-home", methods=["POST", "GET"])
def excel_main_page():
    form = ExcelForm()
    file = form.file.data
    zoom = form.zoom.data
    orientation = form.orientation.data
    page_size = form.page_size.data
    format = form.format.data
    if request.method == "POST":
        if file.content_type not in content_type:
            flash("This is not an excel file", category="error")
        else:
            try:
                print(format)
                filename = secure_filename(file.filename)
                name = file.filename.split(".")[0]
                upload_dir = os.path.join(current_app.root_path, "static", "files")
                pdf_dir = os.path.join(current_app.root_path, "static", "pdf_files")
                os.makedirs(upload_dir, exist_ok=True)
                os.makedirs(pdf_dir, exist_ok=True)

                file_path = os.path.join(upload_dir, filename)
                pdf_path = os.path.join(pdf_dir, f"{name}.pdf")
                word_path = os.path.join(pdf_dir, f"{name}.docx")
                file.save(file_path)

                path_wkhtmltopdf = os.path.join(current_app.root_path, "wkhtmltopdf.exe")
                if format == "PDF":
                    convert_excel_to_pdf(file_path, pdf_path, zoom=zoom, page_size=page_size, orientation=orientation,
                                         path=path_wkhtmltopdf)
                    if os.path.exists(pdf_path):
                        print("PDF file exists:", pdf_path)
                        return send_file(pdf_path, as_attachment=True, download_name=f"{name}.pdf")
                    else:
                        print("PDF file does not exist:", pdf_path)
                        flash("Failed to create PDF file.", category="error")
                else:
                    convert_excel_to_pdf(file_path, pdf_path, zoom=zoom, page_size=page_size, orientation=orientation,
                                         path=path_wkhtmltopdf)
                    convert_pdf_to_word(pdf_path, word_path)
                    if os.path.exists(word_path):
                        print("Word file exists:", word_path)
                        return send_file(word_path, as_attachment=True, download_name=f"{name}.docx")
                    else:
                        print("Word file does not exist:", word_path)
                        flash("Failed to create Word file.", category="error")
            except Exception as e:
                print(str(e))
                flash("An error occurred!!", category="error")
    return render_template('excel_templates/excel_home.html', form=form)
