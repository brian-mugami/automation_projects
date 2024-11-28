from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ReadingForm(FlaskForm):
    word_file = FileField('Upload Word File', validators=[
        FileRequired(message="Select a word file."),
        FileAllowed(['doc', 'docx'], message="Only Word files are allowed!")
    ])
