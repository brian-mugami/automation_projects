import os

from flask import Blueprint, render_template, request, flash, current_app, send_file
from werkzeug.utils import secure_filename

from .pagination_form import PaginationForm
from ...side_proj_6 import paginate_pdf
pager_blp = Blueprint("pager_blp", __name__)
PAGE_ERROR = "The from page number must be lesser then the to page number"
NOT_PDF = "This file is not a pdf"


@pager_blp.route("/page-home", methods=["POST","GET"])
def pager_main_page():
    form = PaginationForm()
    from_no = form.from_no.data
    to_no = form.to_no.data
    file = form.file.data
    if request.method == "POST":
        if file.content_type != "application/pdf":
            flash(NOT_PDF, category="error")
        elif to_no and from_no and to_no <= from_no:
            flash(PAGE_ERROR, category="error")
        else:
            filename = secure_filename(file.filename)
            name = file.filename.split(".")
            upload_dir = os.path.join(current_app.root_path, "static", "files")
            pager_dir = os.path.join(current_app.root_path, "static", "paged_files")

            os.makedirs(upload_dir, exist_ok=True)
            os.makedirs(pager_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, filename)
            paginated_path = os.path.join(pager_dir, f"{name}_paginated_from _{from_no}.pdf")
            file.save(file_path)

            paginate_pdf(file_path, paginated_path, from_no, to_no)
            if os.path.exists(paginated_path):
                print("Initialized file exists:", paginated_path)
                return send_file(paginated_path, as_attachment=True,
                                 download_name=f"{name}_paginated_from_{from_no}.pdf")
            else:
                print("Initialized file does not exist:", paginated_path)
                flash("Failed to create Initialized File.", category="error")
    return render_template('initial_templates/pager_home.html', form=form)
