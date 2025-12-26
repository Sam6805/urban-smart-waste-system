from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret123"

# ================= IMAGE UPLOAD CONFIG =================
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ================= MYSQL CONNECTION =================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Shrija@04",
        database="smart_garbage"
    )

# ================= CREATE TABLES ===========S======
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            phone VARCHAR(15),
            address TEXT,
            area VARCHAR(50),
            username VARCHAR(50) UNIQUE,
            password VARCHAR(255)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reports(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            description TEXT,
            image VARCHAR(255),
            latitude VARCHAR(50),
            longitude VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

init_db()

# ================= REGISTRATION =================
@app.route("/")
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_user():
    fullname = request.form.get("fullname")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")
    area = request.form.get("area")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        return render_template("register.html", error="Passwords do not match!")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email=%s OR username=%s", (email, username))
    if cur.fetchone():
        return render_template("register.html", error="User already exists!")

    cur.execute("""
        INSERT INTO users(fullname,email,phone,address,area,username,password)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (fullname, email, phone, address, area, username, password))

    conn.commit()
    user_id = cur.lastrowid
    cur.close()
    conn.close()

    session["user_id"] = user_id
    session["username"] = username

    return redirect(url_for("report_garbage"))

# ================= REPORT GARBAGE PAGE =================
@app.route("/user")
def report_garbage():
    if "user_id" not in session:
        return redirect(url_for("register_page"))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT fullname, phone FROM users WHERE id=%s", (session["user_id"],))
    user = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(
        "reportgarbage.html",
        name=user["fullname"],
        phone=user["phone"]
    )

# ================= SUBMIT REPORT =================
@app.route("/submit-report", methods=["POST"])
def submit_report():
    if "user_id" not in session:
        return redirect(url_for("register_page"))

    description = request.form.get("description")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    image = request.files.get("image")
    image_name = None

    if image:
        image_name = secure_filename(image.filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_name))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports(user_id, description, image, latitude, longitude)
        VALUES (%s,%s,%s,%s,%s)
    """, (session["user_id"], description, image_name, latitude, longitude))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("my_reports"))

# ================= MY REPORTS =================
@app.route("/my-reports")
def my_reports():
    if "user_id" not in session:
        return redirect(url_for("register_page"))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT reports.*, users.fullname, users.phone
        FROM reports
        JOIN users ON reports.user_id = users.id
        WHERE users.id = %s
        ORDER BY created_at DESC
    """, (session["user_id"],))

    reports = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("Myreport.html", reports=reports)

# ================= PROFILE =================
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("register_page"))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE id=%s", (session["user_id"],))
    user = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("profile.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("register_page"))


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)