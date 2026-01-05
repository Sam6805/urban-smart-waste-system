from flask import Blueprint, render_template, session, redirect, url_for , request, current_app, flash
from .models import get_db_connection
import os
from werkzeug.utils import secure_filename
import json

user_view = Blueprint('user_view', __name__)

@user_view.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.user_login'))

@user_view.route('/user_reportpage',methods=['GET','POST'])
def user_reportpage():
    if 'user_id' not in session:
        return redirect(url_for('auth.user_login'))

    if request.method == 'POST':
        photo = request.files.get("Photo")
        description = request.form.get("description", "")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
   
        if latitude and longitude:
            location = json.dumps({"latitude": latitude, "longitude": longitude})
        else:
            location = json.dumps({})
        
        photo_filename = ""
        if photo and photo.filename:
            photo_filename = secure_filename(photo.filename)
            photo_filename = f"{photo_filename}"
            upload_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], photo_filename)
            photo.save(upload_path)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """INSERT INTO report 
                   (id, userId, userName, userPhone, userAddress, photoUrl, description, status, location) 
                   VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        values = (
            session.get('user_id'),
            session.get('user_name'),
            session.get('user_phone'),
            session.get('user_address'),
            photo_filename,
            description,
            'Pending',
            location,     
        )
        
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()
        
        flash('Report submitted successfully!', 'success')
        return redirect(url_for('user_view.user_myreport'))
    
    return render_template(
        'user-reportpage.html',
        user_name = session.get('user_name'),
        phone_no = session.get('user_phone')
    )


@user_view.route('/user_myreport')
def user_myreport():
    if 'user_id' not in session:
        return redirect(url_for('auth.user_login'))
    
    # Fetch all reports for the logged-in user
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    query = """SELECT * FROM report 
               WHERE userId = %s 
               ORDER BY id DESC"""
    
    cur.execute(query, (session.get('user_id'),))
    reports = cur.fetchall()
    
    # Parse JSON location and format date for each report
    for report in reports:
        if report.get('location'):
            try:
                report['location_data'] = json.loads(report['location'])
            except:
                report['location_data'] = {}
        else:
            report['location_data'] = {}
        
        # Format the created date
        if report.get('createdAt'):
            report['formatted_date'] = report['createdAt'].strftime('%m/%d/%Y %I:%M %p')
        else:
            report['formatted_date'] = 'N/A'
    
    cur.close()
    conn.close()

    return render_template('user-reportstat.html', reports=reports)

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

