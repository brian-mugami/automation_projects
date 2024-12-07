from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, MultipleFileField, IntegerField, SubmitField, FieldList
from wtforms.validators import DataRequired, NumberRange, ValidationError


class FileEntryForm(FlaskForm):
    file = FileField("Select Main PDF File", validators=[
        FileRequired(message="Please select the main PDF file."),
        FileAllowed(['pdf'], message="Only PDF files are allowed!")
    ])
    files = MultipleFileField("Select PDFs to Insert", validators=[
        FileRequired(message="Please upload the PDFs to be merged."),
        FileAllowed(['pdf'], message="Only PDF files are allowed!")
    ])
    page_numbers = FieldList(
        IntegerField("Insert At (Page Number)", validators=[
            DataRequired(message="Please specify the page number."),
            NumberRange(min=1, message="Page number must be greater than 0.")
        ]),
        min_entries=1
    )
    submit = SubmitField("Merge PDFs")

    def validate_page_numbers(self, field):
        if len(self.files.data) != len(field.entries):
            raise ValidationError("Each file must have a corresponding page number.")
