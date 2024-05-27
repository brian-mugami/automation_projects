from flask import Blueprint, render_template, session

home_blp = Blueprint("home_blp", __name__)


@home_blp.route("/")
def homepage():
    session.pop("num_items", None)
    return render_template('home.html')
