from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired


class PaginationForm(FlaskForm):
    from_no = StringField("From Number",default="1", validators=[DataRequired()])
    to_no = IntegerField("To Number")
    file = FileField('Upload PDF File', validators=[
        FileRequired(message="Select a pdf file."),
        FileAllowed(['pdf'], message="Only PDF files are allowed!")
    ])
    x_offset = IntegerField("X offset", default=50)
    y_offset = IntegerField("Y offset", default=20)
    submit = SubmitField("Upload")
