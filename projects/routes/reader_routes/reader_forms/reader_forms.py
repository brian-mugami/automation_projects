from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import ValidationError


class PDFForm(FlaskForm):
    file = FileField('Upload PDF File', validators=[
        FileRequired(message="Select a pdf file."),
        FileAllowed(['pdf'], message="Only PDF files are allowed!")
    ])
    from_page = IntegerField("From Page")
    to_page = IntegerField("To Page")
    page = IntegerField("Page to read on pdf")
    submit = SubmitField("Upload")

    def validate(self):
        if not super().validate():
            return False

        from_page = self.from_page.data
        to_page = self.to_page.data

        if (from_page and not to_page) or (to_page and not from_page):
            raise ValidationError('Both "From Page" and "To Page" are required if either is provided.')

        return True
