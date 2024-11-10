from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms.fields.choices import SelectField, RadioField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, NumberRange


class ExcelForm(FlaskForm):
    file = FileField('Upload Excel File To Convert to PDF', validators=[
        FileRequired(message="Select an excel file."),
        FileAllowed(['xlsx', 'xlsm', 'xls'], message="Only Excel files are allowed!")
    ])
    orientation = SelectField("Orientation", choices=[("Landscape", "Landscape"), ("Portrait", "Portrait")])
    page_size = SelectField('Page Size', choices=[
        ('A4', 'A4'), ('Letter', 'Letter'), ('Legal', 'Legal'),
        ('A3', 'A3'), ('A5', 'A5'), ('Tabloid', 'Tabloid')
    ], default='A4', validators=[DataRequired()])
    zoom = FloatField('Zoom', default=1.0, validators=[DataRequired(), NumberRange(min=0.5, max=3.0,
                                                                                   message="Zoom must be between 0.5 and 3.0")]
                      )
    format = RadioField("Extract Format", choices=[("PDF", "PDF"), ("Word", "Word")])
    submit = SubmitField("Upload")
