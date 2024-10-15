from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired


class PaginationForm(FlaskForm):
    from_no = IntegerField("From Number", default=1, validators=[DataRequired()])
    to_no = IntegerField("To Number")
    file = FileField('Upload PDF File', validators=[
        FileRequired(message="Select a pdf file."),
        FileAllowed(['pdf'], message="Only PDF files are allowed!")
    ])
    submit = SubmitField("Upload")
