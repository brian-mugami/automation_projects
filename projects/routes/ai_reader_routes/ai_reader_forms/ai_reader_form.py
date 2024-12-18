from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired


class ReadingForm(FlaskForm):
    word_file = FileField('Upload Word File', validators=[
        FileRequired(message="Select a word file."),
        FileAllowed(['doc', 'docx'], message="Only Word files are allowed!")
    ])


class ParsingForm(FlaskForm):
    option = SelectField("Section for use to parse the document", choices=[
        ("text_boxes", "text_boxes"), ("body", "body"), ("tables", "tables"), ("headings", "headings"),
        ("headers", "headers"), ("footers", "footers")
    ])
    description = TextAreaField("What can we do for you", validators=[DataRequired()])
    model = SelectField("Choose model to use", choices=[("Ollama", "Ollama")])
