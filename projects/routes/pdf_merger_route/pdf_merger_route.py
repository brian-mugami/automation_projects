import os

from flask import Blueprint, request, flash, current_app, send_file, render_template
from werkzeug.utils import secure_filename

from .pdf_merger_form import FileEntryForm
from ...resources.merge_pdf_exact_page import merge_multiple_pdfs, PDFMergeException

merge_blp = Blueprint("merge_blp", __name__)


@merge_blp.route("/merge", methods=["GET", "POST"])
def merge_pdf():
    form = FileEntryForm()
    if form.validate_on_submit():
        main_pdf = form.file.data
        merge_pdfs = form.files.data

        if main_pdf.content_type != "application/pdf":
            flash("Main file is not a PDF", category="error")
            return render_template("pdf_merged_templates/merge_pdfs.html", form=form)

        upload_dir = os.path.join(current_app.root_path, "static", "files")
        os.makedirs(upload_dir, exist_ok=True)

        main_pdf_path = os.path.join(upload_dir, secure_filename(main_pdf.filename))
        main_pdf.save(main_pdf_path)

        uploaded_files = []
        page_numbers = []

        for i, uploaded_file in enumerate(merge_pdfs):
            if uploaded_file.content_type != "application/pdf":
                flash(f"File {uploaded_file.filename} is not a PDF", category="error")
                return render_template("pdf_merged_templates/merge_pdfs.html", form=form)

            uploaded_file_path = os.path.join(upload_dir, secure_filename(uploaded_file.filename))
            uploaded_file.save(uploaded_file_path)
            uploaded_files.append(uploaded_file_path)

            page_number_field = f"page_numbers-{i}"
            page_number = int(request.form.get(page_number_field, 0))
            if page_number <= 0:
                flash(f"Invalid page number for file {uploaded_file.filename}", category="error")
                return render_template("pdf_merged_templates/merge_pdfs.html", form=form)
            page_numbers.append(page_number)

        if len(uploaded_files) != len(page_numbers):
            flash("Number of files and page numbers do not match", "error")
            return render_template("pdf_merged_templates/merge_pdfs.html", form=form)

        merged_file_path = os.path.join(upload_dir, "merged_output.pdf")
        try:
            merge_multiple_pdfs(
                main_pdf_path, merged_file_path, list(zip(uploaded_files, page_numbers))
            )
            flash("PDFs merged successfully!", "success")
            return send_file(merged_file_path, as_attachment=True)
        except PDFMergeException as e:
            flash(str(e), category="error")
        except Exception as e:
            flash(f"Unexpected error: {e}", "error")

    return render_template("pdf_merged_templates/merge_pdfs.html", form=form)
