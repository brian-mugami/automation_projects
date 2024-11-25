from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms.fields.choices import SelectField, RadioField

from projects.utils import language_choices


class TranslationForm(FlaskForm):
    word_file = FileField('Upload Word File', validators=[
        FileRequired(message="Select a word file."),
        FileAllowed(['doc', 'docx'], message="Only Word files are allowed!")
    ])
    language = SelectField("What Language To Translate To?", choices=language_choices)
    model = RadioField("Model to use", choices=[("googletrans", "googletrans"), ("model2", "model2"), ("model3", "model3"),
                                                ("model4", "model4"), ])
    translate = SubmitField("Translate")
