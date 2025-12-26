from flask import Blueprint, render_template, session, redirect, url_for
from .models import get_db_connection

user_view = Blueprint('user_view', __name__)

@user_view.route('/')
def index():
    return redirect(url_for('auth.login'))

@user_view.route('/user_reportpage')
def user_reportpage():
    if 'user_id' not in session:
        return redirect(url_for('auth.user_login'))
    return render_template('user-reportpage.html')