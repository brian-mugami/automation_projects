from flask import Flask


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_pyfile('default_config.py')

    from .routes import reader_blp, home_blp, quote_blp

    app.register_blueprint(reader_blp, url_prefix="/reader")
    app.register_blueprint(home_blp, url_prefix="/")
    app.register_blueprint(quote_blp, url_prefix="/quote")
    return app
