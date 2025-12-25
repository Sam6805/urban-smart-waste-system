from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")


    from .auth import auth
    from .view import view

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(view, url_prefix='/')

    return app
