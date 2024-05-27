import os

from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

SECRET_KEY = os.environ.get("APP_SECRET_KEY")
PROPAGATE_EXCEPTIONS = True
DEBUG = True
UPLOAD_FOLDER = "static/files"
