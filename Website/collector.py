from flask import Blueprint, render_template, session, redirect, url_for
from .models import get_db_connection

collector_view = Blueprint('collector_view', __name__)

@collector_view.route('/')
def index():
    return redirect(url_for('auth.login'))

@collector_view.route('/collector_homescreen')
def collector_homescreen():
    if 'collector_id' not in session:
        return redirect(url_for('auth.collector_login'))
    return render_template('collector-homescreen.html')