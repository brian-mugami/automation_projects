from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms.fields.numeric import IntegerField


class PDFForm(FlaskForm):
    file = FileField('Upload PDF File', validators=[
        FileRequired(message="Select a pdf file."),
        FileAllowed(['pdf'], message="Only PDF files are allowed!")
    ])
    word_file = FileField('Upload Word File', validators=[
        FileRequired(message="Select a word file."),
        FileAllowed(['doc', 'docx'], message="Only Word files are allowed!")
    ])
    from_page = IntegerField("From Page")
    to_page = IntegerField("To Page")
    page = IntegerField("Page to read on pdf")
    submit = SubmitField("Upload")
