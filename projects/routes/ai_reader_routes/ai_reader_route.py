import os

from flask import Blueprint, render_template, jsonify, flash, current_app, request

from .ai_reader_forms import ReadingForm

ai_blp = Blueprint("ai_blp", __name__)

content_type = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
    "application/msword",
]


@ai_blp.route("/")
def ai_home():
    return render_template("ai_templates/ai_home.html",)


@ai_blp.route("/word", methods=["POST", "GET"])
def ai_word():
    form = ReadingForm()
    file = form.word_file.data
    if request.method == "POST":
        if file.content_type not in content_type:
            flash("This is not a word document",category="error" )
        name = file.filename.split(".")[0]
        word_dir = os.path.join(current_app.root_path, "static", "word_files")
        os.makedirs(word_dir, exist_ok=True)
        word_path = os.path.join(word_dir, f"{name}.docx")
        file.save(word_path)

    return render_template("ai_templates/word_reader.html", form=form)
