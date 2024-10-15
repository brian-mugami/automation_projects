from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


class ExcelForm(FlaskForm):
    file = FileField('Upload Excel File To Convert to PDF', validators=[
        FileRequired(message="Select an excel file."),
        FileAllowed(['xlsx', 'xlsm', 'xls'], message="Only Excel files are allowed!")
    ])
    submit = SubmitField("Upload")
