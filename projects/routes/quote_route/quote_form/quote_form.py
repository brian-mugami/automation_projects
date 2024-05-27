from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DateField, IntegerField, FloatField, StringField, FormField, FieldList
from wtforms.validators import DataRequired, Optional

from .choices import currency_choices


class QuoteLineForm(FlaskForm):
    discount = FloatField("Discount Per Item", validators=[Optional()], default=0)


class QuoteForm(FlaskForm):
    items = IntegerField("Number of Items in Quote", validators=[DataRequired()])
    VAT = FloatField("VAT (%) on Items in Quote", validators=[DataRequired()])
    other = FloatField("Other Tax (%) on Items in Quote", default=0)
    margin = FloatField("Margin to Be Applied", validators=[DataRequired()])
    customer_name = StringField("Customer Name", validators=[DataRequired()])
    customer_contact = StringField("Customer Contact Person", validators=[DataRequired()])
    customer_site = StringField("Customer Site", validators=[DataRequired()])
    quote_date = DateField("Quote Date", validators=[DataRequired()], default=datetime.utcnow)
    sales_support = StringField("Sales Support", validators=[DataRequired()])
    account_manager = StringField("Account Manager", validators=[DataRequired()])
    default_currency = SelectField("Currency of the Quote", validators=[DataRequired()], choices=currency_choices,
                                   default='KES')
    conversion_currency = SelectField("Conversion Currency", choices=currency_choices)
    conversion_rate = FloatField("Conversion Rate")
    quote_lines = FieldList(FormField(QuoteLineForm), min_entries=1)
    submit = SubmitField("Create Quote")
