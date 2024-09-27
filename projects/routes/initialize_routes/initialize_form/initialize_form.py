from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, MultipleFileField
from wtforms import SubmitField, StringField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired

from .choices import choices


class InitialForm(FlaskForm):
    initial = StringField("Initial", validators=[DataRequired()])
    size = IntegerField("Font Size", default=12, validators=[DataRequired()])
    x_axis = IntegerField("X-Axis", default=0)
    y_axis = IntegerField("Y-Axis", default=0)
    file = FileField('Upload PDF File', validators=[
        FileRequired(message="Select a pdf file."),
        FileAllowed(['pdf'], message="Only PDF files are allowed!")
    ])
    multiple_files = MultipleFileField('Upload PDF File', validators=[
        FileRequired(message="Select a pdf file."),
        FileAllowed(['pdf'], message="Only PDF files are allowed!")
    ])
    font = SelectField("Font", choices=choices)
    submit = SubmitField("Upload")


class ImageInitialForm(FlaskForm):
    initial_image = FileField('Upload Image Initial', validators=[
        FileRequired(message="Select an image."),
        FileAllowed(['jpg', 'png', 'jpeg'], message="Only Images are allowed!")
    ])
    img_width = IntegerField("Image Width", default=30)
    img_height = IntegerField("Image Height", default=30)
    x_axis = IntegerField("X-Axis", default=0)
    y_axis = IntegerField("Y-Axis", default=0)
    file = FileField('Upload PDF File', validators=[
        FileRequired(message="Select a pdf file."),
        FileAllowed(['pdf'], message="Only PDF files are allowed!")
    ])
    multiple_files = MultipleFileField('Upload PDF Files', validators=[
        FileRequired(message="Select a pdf files."),
        FileAllowed(['pdf'], message="Only PDF files are allowed!")
    ])
    submit = SubmitField("Upload")
