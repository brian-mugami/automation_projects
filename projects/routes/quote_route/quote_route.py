from datetime import datetime

from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired

from .quote_form import QuoteForm

quote_blp = Blueprint("quote_blp", __name__)
CREATION_SUCCESS = "Quote created successfully"


class QuoteLineForm(FlaskForm):
    discount = FloatField("Discount(%)", default=0)
    item_name = StringField("Item Name", validators=[DataRequired()])
    item_description = StringField("Item Description", validators=[DataRequired(), ])
    item_price = FloatField("Item Price", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    logistics_fee = FloatField("Logs(%)")
    duties_fee = FloatField("Duties(%)")
    other_fee = FloatField("Other(%)")


@quote_blp.route('/quote', methods=['GET', 'POST'])
def create_quote():
    num_items = session.get('num_items', 0)
    counter = session.get('counter', 0)
    data = session.get("form_data", None)
    conversion = ""

    class LocalForm(QuoteForm):
        pass

    LocalForm.quote_lines = FieldList(FormField(QuoteLineForm), min_entries=num_items)
    print(counter)
    print(data)

    form = LocalForm()
    if 'form_data' in session:
        form_data = session['form_data']
        for field_name, value in form_data.items():
            if hasattr(form, field_name):
                if field_name == 'quote_date':
                    getattr(form, field_name).data = datetime.strptime(value, '%Y-%m-%d')
                else:
                    getattr(form, field_name).data = value
    if request.method == "POST" and counter == 0:
        if 'items' in request.form:
            if len(form.conversion_currency.data) > 2:
                conversion = True
            else:
                conversion = False
            num_items = form.items.data
            counter += 1
            session['counter'] = counter
            session['num_items'] = num_items
            session['form_data'] = request.form.to_dict()
            return redirect(url_for('quote_blp.create_quote'))

    if request.method == "POST" and counter != 0:
        conversion = True
        session.pop("num_items", None)
        session.pop("counter", None)
        session.pop("form_data", None)
        vat = [float(form.VAT.data) if form.VAT.data is not None else 0]
        margin = float(form.margin.data)
        other_tax = [float(form.other.data) if form.other.data is not None else 0]
        total_tax = 1 + ((vat[0] + other_tax[0]) / 100)
        total = 0
        conversion_rate = 0
        if form.conversion_currency.data is not None:
            default_rate = 100
            conversion_rate = [
                float(form.conversion_rate.data) if form.conversion_rate.data is not None else default_rate]
        for line in form.quote_lines:
            print(
                f"{line.item_name.data} - {line.item_description.data} of price {line.item_price.data} and quantity {line.quantity.data}")
            item_total = float(line.item_price.data) * float(line.quantity.data)
            logistics = [float(line.logistics_fee.data) if line.logistics_fee.data is not None else 0]
            duties_fee = [float(line.duties_fee.data) if line.duties_fee.data is not None else 0]
            other_fee = [float(line.other_fee.data) if line.other_fee.data is not None else 0]
            discount = [float(line.discount.data) if line.discount.data is not None else 0]
            add_ons = margin + logistics[0] + duties_fee[0] + other_fee[0]
            actual_discount = 1 - (discount[0] / 100)
            total_add_ons = 1 + (add_ons / 100)
            gross_price = float(item_total * total_add_ons * actual_discount)
            if form.conversion_currency.data:
                conversion_from_currency = form.default_currency.data
                conversion_to_currency = form.conversion_currency.data
                print(f"{conversion_to_currency} from {conversion_from_currency} rate {conversion_rate[0]}")
                gross_price = gross_price / conversion_rate[0]
            print(f"{form.default_currency}")
            print(gross_price)
            total += gross_price
        net_price = total * total_tax
        print(net_price)
        flash(CREATION_SUCCESS, category="success")
        return redirect(url_for('home_blp.homepage'))

    return render_template('quote_templates/quote_template.html', form=form, counter=counter, conversion=conversion)
