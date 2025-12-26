from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from .models import get_db_connection

auth = Blueprint('auth', __name__)

# Admin Signup Route
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


#Admin login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        sql = "SELECT * FROM admin WHERE email = %s"
        cur.execute(sql, (email,))
        admin = cur.fetchone()

        if admin and admin['password'] == password:
            session['user_id'] = admin['id']
            session['user_name'] = admin['name']
            return redirect(url_for('admin_view.dashboard'))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))


    return render_template('admin-login.html')


#User Signup Route
@auth.route('/user_signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
       fullname = request.form.get("fullName")
       email = request.form.get("email")
       phone = request.form.get("phone")
       address = request.form.get("address")
       username = request.form.get("userName")
       password = request.form.get("password")

       conn = get_db_connection()
       cur = conn.cursor()

       sql = "SELECT * FROM users WHERE email=%s OR username=%s"
       cur.execute(sql, (email,username))
       user = cur.fetchone()

       if user:
           flash("Email or Username already exists","danger")
           return redirect(url_for('auth.user_login'))
       
       sql = """
       INSERT INTO users(name,username,email,phone_no,password,address)
       VALUES (%s,%s,%s,%s,%s,%s)
       """
       val = (fullname,username, email, phone, password, address)

       try:
           cur.execute(sql, val)
           conn.commit()
           flash("Account created successfully!", "success")
           return redirect(url_for('auth.user_login'))
       except Exception as e:
           flash("Something went wrong. Try again.", "danger")
           print("Error:", e)
       finally:
           cur.close()
           conn.close()
           
       
    return render_template('user-signup.html')

#User Login Route
@auth.route("/user_login", methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        sql = "SELECT * FROM users WHERE email = %s"
        cur.execute(sql, (email,))
        user = cur.fetchone()

        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('user_view.user_reportpage'))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))
    return render_template("user-login.html")


# Collector SignUp Route
@auth.route("/collector_signup", methods=['GET', 'POST'])
def collector_signup():
    if request.method == 'POST':
       name = request.form["name"]
       phone = request.form["phone"]
       vehicle_no = request.form["vehicle_no"]
       email = request.form["email"]
       area = request.form["area"]
       password = request.form["password"]

    
       conn = get_db_connection()
       cur = conn.cursor()

       sql = "SELECT * FROM collector WHERE email=%s OR vehicle_no=%s"
       cur.execute(sql, (email,vehicle_no))
       user = cur.fetchone()

       if user:
           flash("Email or Vehicle No. already exists","danger")
           return redirect(url_for('auth.collector_signup'))
       
       sql = """
       INSERT INTO collector(name,email, phone_no, password, vehicle_no, area) 
       VALUES (%s,%s,%s,%s,%s,%s)
       """

       val = (name, email, phone, password, vehicle_no, area)

       try:
           cur.execute(sql, val)
           conn.commit()
           flash("Account created successfully!", "success")
           return redirect(url_for('auth.collector_login'))
       except Exception as e:
           flash("Something went wrong. Try again.", "danger")
           print("Error:", e)
       finally:
           cur.close()
           conn.close()
    return render_template("collector-signup.html")


# Collector Login Route
@auth.route("/collector_login", methods=['GET', 'POST'])
def collector_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        sql = "SELECT * FROM collector WHERE email = %s"
        cur.execute(sql, (email,))
        collector = cur.fetchone()

        if collector and collector['password'] == password:
            session['collector_id'] = collector['id']
            session['collector_name'] = collector['name']
            return redirect(url_for('collector_view.collector_homescreen'))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.collector_login"))
    return render_template("collector-login.html")



