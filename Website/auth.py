from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from .models import get_db_connection

auth = Blueprint('auth', __name__)

# Signup Route
@auth.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        name = request.form.get('fullName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor()

        sql = "SELECT * FROM admin WHERE email = %s"
        cur.execute(sql, (email,))
        user = cur.fetchone()

        if user :
            flash("Email already exists","danger")
            return redirect(url_for('auth.admin_signup'))

        sql = """
        INSERT INTO admin (name,email, phone_no, password, address)
        VALUES (%s, %s, %s, %s,%s)
        """
        val = (name,email, phone, password, address)

        try:
            cur.execute(sql, val)
            conn.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash("Something went wrong. Try again.", "danger")
            print("Error:", e)
        finally:
            cur.close()
            conn.close()

    return render_template('admin-signup.html')


#login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_phone = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        sql = "SELECT * FROM admin WHERE email = %s"
        cur.execute(sql, (email_or_phone,))
        user = cur.fetchone()

        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('view.dashboard'))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))


    return render_template('admin-login.html')

@auth.route("/user_login")
def user_login():
    return render_template("user-login.html")

@auth.route('/user_signup')
def user_signup():
    return render_template('user-signup.html')

@auth.route("/collector_login")
def collector_login():
    return render_template("collector-login.html")

@auth.route('/collector_signup')
def collector_signup():
    return render_template('collector-signup.html')


