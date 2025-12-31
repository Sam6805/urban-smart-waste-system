from flask import Blueprint, render_template, session, redirect, url_for , request
from .models import get_db_connection

admin_view = Blueprint('admin_view', __name__)

@admin_view.route('/')
def index():
    return redirect(url_for('auth.login'))


def RegUserList():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute("SELECT * FROM users")
    
    users = cur.fetchall()
    cur.close()
    conn.close()
    
    return users

def collector():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM collector")

    collectors = cur.fetchall()
    cur.close()
    conn.close()

    return collectors

def report():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM report")

    report = cur.fetchall()
    cur.close()
    conn.close()

    return report


@admin_view.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('auth.login'))

    area = request.args.get('area', 'all')   
    status = request.args.get('rstatus')
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()

        if area != 'all':
            cur.execute("SELECT * FROM collector WHERE area = %s", (area,))
        else:
            cur.execute("SELECT * FROM collector")
        collector = cur.fetchall()

        if status:
            cur.execute("SELECT * FROM report WHERE status = %s", (status,))
        else:
            cur.execute("SELECT * FROM report")
        report = cur.fetchall()

        cur.execute("SELECT DISTINCT area FROM collector")
        areas = cur.fetchall()

        cur.execute("SELECT COUNT(*) AS total_report FROM report")
        total_report = cur.fetchone()["total_report"]

        cur.execute("SELECT COUNT(*) AS active_count FROM collector WHERE isActive = 1")
        active_coll = cur.fetchone()["active_count"]

        cur.execute("SELECT COUNT(*) AS pending_report FROM report WHERE status='pending'")
        pending_rep = cur.fetchone()["pending_report"]

        cur.execute("SELECT COUNT(*) AS collected_report FROM report WHERE status='collected'")
        collected_rep = cur.fetchone()["collected_report"]

    finally:
        cur.close()
        conn.close()

    return render_template(
        'admin-dashboard.html',
        users=users,
        collector=collector,
        report=report,
        rstatus=status,
        areas=areas,                
        selected_area=area,          
        active_coll=active_coll,
        pending_rep=pending_rep,
        collected_rep=collected_rep,
        total_report=total_report
    )
