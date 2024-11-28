import os

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from projects.resources.mpesa_statement_reader import read_mpesa_pdf, MpesaStatementException

mpesa_blp = Blueprint("mpesa_blp", __name__)


@mpesa_blp.route("/mpesa_api", methods=["POST"])
def read_mpesa_stat():
    file = request.files['pdf']
    password = request.form.get('password', None)

    if request.method == "POST":
        if file.content_type != "application/pdf":
            return jsonify({'error': 'No PDF file part'}), 400
        else:
            filename = secure_filename(file.filename)
            name = file.filename.split(".")
            upload_dir = os.path.join(current_app.root_path, "static", "files")
            mpesa_dir = os.path.join(current_app.root_path, "static", "mpesa_files")
            os.makedirs(upload_dir, exist_ok=True)
            os.makedirs(mpesa_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            mpesa_path = os.path.join(mpesa_dir, f"{name}_decrypted.pdf")
            file.save(file_path)
            try:
                transaction = read_mpesa_pdf(pdf_path=file_path, pdf_password=password, decrypted_pdf_path=mpesa_path)
                os.remove(file_path)
                os.remove(mpesa_path)
                return jsonify(transaction), 200
            except MpesaStatementException as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 500
