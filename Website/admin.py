from flask import Blueprint, render_template, session, redirect, url_for
from .models import get_db_connection

view = Blueprint('view', __name__)

@view.route('/')
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


@view.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    try:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        
        cur.execute("SELECT * FROM collector")
        collector = cur.fetchall()

        cur.execute("SELECT * FROM report")
        report = cur.fetchall()

        cur.execute("SELECT COUNT(*) AS total_report FROM report")
        Total_report = cur.fetchone()

        total_report = Total_report["total_report"]

        cur.execute("SELECT COUNT(*) AS active_count FROM collector WHERE isActive = 1")
        ActiveColl = cur.fetchone()

        active_coll = ActiveColl['active_count']

        cur.execute("SELECT COUNT(*) AS pending_report FROM report WHERE status = 'pending'")
        Pending_rep = cur.fetchone()

        pending_rep = Pending_rep['pending_report']

        cur.execute("SELECT COUNT(*) AS collected_report FROM report WHERE status = 'collected'")
        Collected_rep = cur.fetchone()

        collected_rep = Collected_rep['collected_report']

    except Exception as e:
        print(f"Error fetching data: {e}")
        users = []
        collector = []
        total_report = 0
        active_coll = 0
        pending_rep = 0
        collected_rep = 0
    finally:
        cur.close()
        conn.close()
    
    return render_template('admin-dashboard.html', users=users, collector=collector, report=report, active_coll=active_coll, pending_rep=pending_rep, collected_rep=collected_rep, total_report=total_report)

