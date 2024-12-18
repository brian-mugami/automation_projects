import json
import os

from flask import Blueprint, render_template, current_app, request, jsonify, session

from .ai_reader_forms import ReadingForm, ParsingForm
from ...resources.parse_docx_with_AI import split_content, parse_with_llama
from ...resources.reading_docx_with_AI import read_word_document

ai_blp = Blueprint("ai_blp", __name__)

content_type = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
    "application/msword",
]


@ai_blp.route("/")
def ai_home():
    return render_template("ai_templates/ai_home.html", )


@ai_blp.route("/word", methods=["POST", "GET"])
def ai_word():
    form = ReadingForm()
    if request.method == "POST":
        file = form.word_file.data
        if not file:
            return jsonify({"success": False, "message": "No file uploaded"}), 400
        if file.content_type not in content_type:
            return jsonify({"success": False, "message": "This is not a Word document"}), 400
        try:
            name = os.path.splitext(file.filename)[0]
            word_dir = os.path.join(current_app.root_path, "static", "word_files")
            os.makedirs(word_dir, exist_ok=True)
            word_path = os.path.join(word_dir, f"{name}.docx")
            file.save(word_path)
            word_data = read_word_document(word_path)
            data_path = os.path.join(word_dir, f"{name}_data.json")
            with open(data_path, "w") as f:
                json.dump(word_data, f)
            session["data_path"] = data_path
            return jsonify({"success": True, "word_data": word_data})
        except Exception as e:
            print(str(e))
            return jsonify({"success": False, "message": f"Error reading document: {str(e)}"}), 500
    return render_template("ai_templates/word_reader.html", form=form)


@ai_blp.route("/parse", methods=["POST", "GET"])
def ai_parse():
    form = ParsingForm()
    section = form.option.data
    model = form.model.data
    description = form.description.data
    data_path = session.get("data_path")
    if not data_path or not os.path.exists(data_path):
        return jsonify({"error": "There is no word document read"})
    with open(data_path, "r") as f:
        data_parsed = json.load(f)
    try:
        if request.method == "POST":
            data = data_parsed.get(section, None)
            if not data:
                return jsonify({"error": f"No Data has been parsed from {section}"})
            else:
                if model == "Ollama":
                    chunks = split_content(data)
                    result = parse_with_llama(chunks, description)
                    print("yes")
                    print(result)
                    return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred during parsing: {str(e)}"}), 500
    return render_template("ai_templates/word_parser.html", form=form)
