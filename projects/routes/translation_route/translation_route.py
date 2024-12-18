import os

from flask import Blueprint, render_template, request, current_app, session, jsonify, flash, Response, \
    stream_with_context, redirect, url_for, send_file

from projects.resources.word_language_detector import detect_word_language
from .translation_form import TranslationForm
from ...resources.translation_deep_translator import translate_word_document_with_deep_translator

translation_blp = Blueprint("translation_blp", __name__)

content_type = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
    "application/msword",
]


@translation_blp.route("/detect", methods=["POST", "GET"])
def language_detector():
    form = TranslationForm()
    dominant_language = None
    if form.word_file.data:
        file = form.word_file.data
        if file.content_type not in content_type:
            return jsonify({"error": "This is not a word file"}), 400

        name = file.filename.split(".")[0]
        session["name"] = name
        word_dir = os.path.join(current_app.root_path, "static", "word_files")
        os.makedirs(word_dir, exist_ok=True)
        word_path = os.path.join(word_dir, f"{name}.docx")
        file.save(word_path)
        session["word"] = word_path
        dominant_language, _ = detect_word_language(word_path)
    if dominant_language:
        return jsonify({"language": dominant_language})
    return render_template("translation_templates/translation.html", form=form)


@translation_blp.route("/translate", methods=["POST", "GET"])
def translator():
    form = TranslationForm()
    path = session.get("word", None)
    target_language = form.language.data
    model = form.model.data
    name = session.get("name", None)

    if request.method == "POST":
        if not path:
            flash("No Word document found for translation!", "error")
            return render_template("translation_templates/translation_page.html", form=form)
        print(target_language)
        print(f"Translating {path} to {target_language} using {model}")
        trans_dir = os.path.join(current_app.root_path, "static", "word_files")
        os.makedirs(trans_dir, exist_ok=True)
        trans_path = os.path.join(trans_dir, f"{name}_translated.docx")

        if model == "Deep Translator":
            try:
                def generate_translation():
                    yield f"data: Translation started to {target_language} using {model} \n\n"
                    for status_update in translate_word_document_with_deep_translator(doc_path=path,
                                                                                      translated_path=trans_path,
                                                                                      target=target_language):
                        yield f"data:{status_update}\n\n"
                    yield "data: Translation completed.\n\n"
                    download_url = url_for('translation_blp.download_translated_file', _external=True)
                    yield f"data: download_url-{download_url}\n\n"

                return Response(stream_with_context(generate_translation()), content_type="text/event-stream")

            except Exception as e:
                flash(f"Error during translation: {str(e)}", "error")
                return render_template("translation_templates/translation_page.html", form=form)
        else:
            flash("Unsupported model selected. Please choose a valid model.", "error")
            return render_template("translation_templates/translation_page.html", form=form)

    return render_template("translation_templates/translation_page.html", form=form)


@translation_blp.route("/download_translated_file", methods=["GET"])
def download_translated_file():
    name = session.get("name")
    trans_dir = os.path.join(current_app.root_path, "static", "word_files")
    trans_path = os.path.join(trans_dir, f"{name}_translated.docx")

    if os.path.exists(trans_path):
        return send_file(trans_path, as_attachment=True, download_name=f"{name}_translated.docx")
    else:
        flash("Translated file not found!", "error")
        return redirect(url_for('translation_blp.translator'))
