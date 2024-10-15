from flask import Flask


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_pyfile('default_config.py')

    from .routes import reader_blp, home_blp, quote_blp, initial_blp, pager_blp, excel_blp

    app.register_blueprint(reader_blp, url_prefix="/reader")
    app.register_blueprint(home_blp, url_prefix="/")
    app.register_blueprint(quote_blp, url_prefix="/quote")
    app.register_blueprint(initial_blp, url_prefix="/initial")
    app.register_blueprint(pager_blp, url_prefix="/pager")
    app.register_blueprint(excel_blp, url_prefix="/excel")
    return app
