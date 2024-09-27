import os
import zipfile
from io import BytesIO

from flask import Blueprint, render_template, request, flash, current_app, send_file
from werkzeug.utils import secure_filename

from .initialize_form import InitialForm, ImageInitialForm
from ...side_proj_5 import add_word_to_pdf, add_image_to_pdf

initial_blp = Blueprint("initial_blp", __name__)
NOT_PDF = "This file is not a pdf"
NOT_IMAGE = "The uploaded initial is not an image"


@initial_blp.route("/initial-home")
def initial_main_page():
    return render_template('initial_templates/initial_home.html')


@initial_blp.route("/initial-many-image", methods=["POST", "GET"])
def many_docs_img_initial():
    form = ImageInitialForm()
    image = form.initial_image.data
    files = form.multiple_files.data
    x_axis = form.x_axis.data
    y_axis = form.y_axis.data
    img_width = form.img_width.data
    img_height = form.img_height.data

    if request.method == "POST":
        output_zip = BytesIO()
        with zipfile.ZipFile(output_zip, "w") as zipf:
            img_filename = secure_filename(image.filename)
            img_name, img_ext = os.path.splitext(img_filename)
            image_dir = os.path.join(current_app.root_path, "static", "initial_images")
            os.makedirs(image_dir, exist_ok=True)
            img_path = os.path.join(image_dir, img_filename)

            image.save(img_path)
            for file in files:
                if file.content_type != "application/pdf":
                    flash(f"The uploaded file '{file.filename}' is not a PDF.", category="error")
                elif not image.content_type.startswith("image/"):
                    flash("The uploaded initial is not a image.", category="error")
                else:
                    pdf_filename = secure_filename(file.filename)
                    pdf_name, pdf_ext = os.path.splitext(pdf_filename)

                    upload_dir = os.path.join(current_app.root_path, "static", "files")
                    initial_dir = os.path.join(current_app.root_path, "static", "initial_files")

                    os.makedirs(upload_dir, exist_ok=True)
                    os.makedirs(initial_dir, exist_ok=True)

                    pdf_file_path = os.path.join(upload_dir, pdf_filename)
                    initialized_path = os.path.join(initial_dir, f"{pdf_name}_initialized_with_{img_name}.pdf")

                    # Save the uploaded Docs
                    file.save(pdf_file_path)

                    # Add initial to the PDF and save the new file
                    add_image_to_pdf(pdf_file_path, initialized_path, img_path, img_width, img_height, x_axis, y_axis)

                    # Add the processed file to the zip archive
                    zipf.write(initialized_path, f"{pdf_name}_initialized_with_{img_name}.pdf")
        output_zip.seek(0)
        return send_file(output_zip, as_attachment=True, download_name="initialized_files.zip",
                         mimetype='application/zip')

    return render_template('initial_templates/initial_many_images.html', form=form)


@initial_blp.route("/initial-image", methods=["POST", "GET"])
def one_doc_img_initial():
    form = ImageInitialForm()
    image = form.initial_image.data
    file = form.file.data
    x_axis = form.x_axis.data
    y_axis = form.y_axis.data
    img_width = form.img_width.data
    img_height = form.img_height.data
    if request.method == "POST":
        if file.content_type != "application/pdf":
            flash("The uploaded file is not a PDF.", category="error")
        elif not image.content_type.startswith("image/"):
            flash("The uploaded initial is not a image.", category="error")
        else:
            pdf_filename = secure_filename(file.filename)
            pdf_name, pdf_ext = os.path.splitext(pdf_filename)
            img_filename = secure_filename(image.filename)
            img_name, img_ext = os.path.splitext(img_filename)

            upload_dir = os.path.join(current_app.root_path, "static", "files")
            initial_dir = os.path.join(current_app.root_path, "static", "initial_files")
            image_dir = os.path.join(current_app.root_path, "static", "initial_images")

            os.makedirs(upload_dir, exist_ok=True)
            os.makedirs(initial_dir, exist_ok=True)
            os.makedirs(image_dir, exist_ok=True)

            pdf_file_path = os.path.join(upload_dir, pdf_filename)
            img_path = os.path.join(image_dir, img_filename)
            initialized_path = os.path.join(initial_dir, f"{pdf_name}_initialized_with_{img_name}.pdf")

            # Save the uploaded Docs
            file.save(pdf_file_path)
            image.save(img_path)

            add_image_to_pdf(pdf_file_path, initialized_path, img_path, img_width, img_height, x_axis, y_axis)
            if os.path.exists(initialized_path):
                print("Initialized file exists:", initialized_path)
                return send_file(initialized_path, as_attachment=True,
                                 download_name=f"{pdf_name}_initialized_with_{img_name}.pdf")
            else:
                print("Initialized file does not exist:", initialized_path)
                flash("Failed to create Initialized File.", category="error")
    return render_template('initial_templates/initial_one_image.html', form=form)


@initial_blp.route("/one_doc_initial", methods=["POST", "GET"])
def one_doc_initial():
    form = InitialForm()
    if request.method == "POST":
        size = form.size.data
        initial = form.initial.data
        x_axis = form.x_axis.data
        y_axis = form.y_axis.data
        font = form.font.data
        file = form.file.data

        # Check if file is a PDF
        if file.content_type != "application/pdf":
            flash("The uploaded file is not a PDF.", category="error")
        else:
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)  # Separate name and extension
            upload_dir = os.path.join(current_app.root_path, "static", "files")
            initial_dir = os.path.join(current_app.root_path, "static", "initial_files")

            # Create directories if they don't exist
            os.makedirs(upload_dir, exist_ok=True)
            os.makedirs(initial_dir, exist_ok=True)

            # Define paths
            file_path = os.path.join(upload_dir, filename)
            initialized_path = os.path.join(initial_dir, f"{name}_initialized_with_{initial}.pdf")

            # Save the uploaded PDF
            file.save(file_path)

            # Add initial to the PDF and save the new file
            add_word_to_pdf(file_path, initialized_path, initial, font, size, x_axis, y_axis)
            # Check if the initialized file exists
            if os.path.exists(initialized_path):
                print("Initialized file exists:", initialized_path)
                return send_file(initialized_path, as_attachment=True,
                                 download_name=f"{name}_initialized_with_{initial}.pdf")
            else:
                print("Initialized file does not exist:", initialized_path)
                flash("Failed to create Initialized File.", category="error")

    return render_template('initial_templates/initial_one_page.html', form=form)


@initial_blp.route("/many_doc_initial", methods=["POST", "GET"])
def many_doc_initial():
    form = InitialForm()
    size = form.size.data
    initial = form.initial.data
    x_axis = form.x_axis.data
    y_axis = form.y_axis.data
    font = form.font.data
    many_files = form.multiple_files.data
    if request.method == "POST":
        output_zip = BytesIO()
        with zipfile.ZipFile(output_zip, "w") as zipf:
            for file in many_files:
                if file.content_type != "application/pdf":
                    flash(f"The uploaded file '{file.filename}' is not a PDF.", category="error")
                else:
                    filename = secure_filename(file.filename)
                    name, ext = os.path.splitext(filename)  # Separate name and extension
                    upload_dir = os.path.join(current_app.root_path, "static", "files")
                    initial_dir = os.path.join(current_app.root_path, "static", "multiple_initial_files")

                    # Create directories if they don't exist
                    os.makedirs(upload_dir, exist_ok=True)
                    os.makedirs(initial_dir, exist_ok=True)

                    # Define paths
                    file_path = os.path.join(upload_dir, filename)
                    initialized_path = os.path.join(initial_dir, f"{name}_initialized_with_{initial}.pdf")

                    # Save the uploaded PDF
                    file.save(file_path)

                    # Add initial to the PDF and save the new file
                    add_word_to_pdf(file_path, initialized_path, initial, font, size, x_axis, y_axis)

                    # Add the processed file to the zip archive
                    zipf.write(initialized_path, f"{name}_initialized_with_{initial}.pdf")
        output_zip.seek(0)
        return send_file(output_zip, as_attachment=True, download_name="initialized_files.zip",
                         mimetype='application/zip')
    return render_template('initial_templates/initial_many_pages.html', form=form)
