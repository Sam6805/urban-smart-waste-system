from flask import Blueprint, render_template, session, redirect, url_for
from .models import get_db_connection

user_view = Blueprint('user_view', __name__)

@user_view.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.user_login'))

@user_view.route('/user_reportpage')
def user_reportpage():
    if 'user_id' not in session:
        return redirect(url_for('auth.user_login'))

    

    return render_template(
        'user-reportpage.html',
        user_name = session.get('user_name'),
        phone_no = session.get('user_phone')
    )

@user_view.route('/user_myreport')
def user_myreport():

    return render_template('user-reportstat.html')

@user_view.route('/user_profile')
def user_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.user_login'))
    

    return render_template(
        'user-profile.html',
        user_name = session.get('user_name'),
        phone_no = session.get('user_phone'),
        user_email = session.get('user_email'),
        user_address = session.get('user_address')
        )
