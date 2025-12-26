from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")


    from .auth import auth
    from .admin import admin_view
    from .user import user_view
    from .collector import collector_view

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin_view, url_prefix='/')
    app.register_blueprint(user_view, url_prefix='/')
    app.register_blueprint(collector_view, url_prefix='/')

    return app
