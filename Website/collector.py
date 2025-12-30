from flask import Blueprint, render_template, session, redirect, url_for
from .models import get_db_connection

collector_view = Blueprint('collector_view', __name__)

@collector_view.route('/collector_homescreen')
def collector_homescreen():
    if 'collector_id' not in session:
        return redirect(url_for('auth.collector_login'))

    collector_name = session.get('collector_name')
    vehicle_no = session.get('vehicle_no')

    return render_template(
        'collector-homescreen.html',
        collector_name=collector_name,
        vehicle_no=vehicle_no
    )
