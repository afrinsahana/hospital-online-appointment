from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb
import config
import re

app = Flask(__name__)
app.secret_key = "hospital-appointment-secret-key"


def get_db():
    return MySQLdb.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        passwd=config.MYSQL_PASSWORD,
        db=config.MYSQL_DB,
        cursorclass=MySQLdb.cursors.DictCursor
    )


@app.route("/")
def index():
    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO patients
                (name, email, phone, password)
                VALUES (%s, %s, %s, %s)
                """,
                (name, email, phone, hashed_password)
            )

            db.commit()

            flash("Registration successful. Please login.", "success")
            return redirect(url_for("login"))

        except Exception:
            db.rollback()
            flash("Email already registered.", "danger")

        finally:
            cursor.close()
            db.close()

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM patients WHERE email=%s",
            (email,)
        )

        patient = cursor.fetchone()

        cursor.close()
        db.close()

        if patient and check_password_hash(
            patient["password"], password
        ):

            session["patient_id"] = patient["id"]
            session["patient_name"] = patient["name"]

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "patient_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        name=session["patient_name"]
    )


# ---------------- HOSPITALS ----------------

@app.route("/hospitals")
def hospitals():

    department = request.args.get("department")

    db = get_db()
    cursor = db.cursor()

    if department:

        cursor.execute(
            """
            SELECT * FROM hospitals
            WHERE department=%s
            """,
            (department,)
        )

    else:

        cursor.execute(
            "SELECT * FROM hospitals"
        )

    hospitals = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "hospitals.html",
        hospitals=hospitals
    )


# ---------------- DOCTORS ----------------

@app.route("/doctors/<int:hospital_id>")
def doctors(hospital_id):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT doctors.*, hospitals.name AS hospital_name
        FROM doctors
        JOIN hospitals
        ON doctors.hospital_id = hospitals.id
        WHERE hospitals.id=%s
        """,
        (hospital_id,)
    )

    doctors = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "doctors.html",
        doctors=doctors
    )


# ---------------- APPOINTMENT ----------------

@app.route("/appointment/<int:doctor_id>", methods=["GET", "POST"])
def appointment(doctor_id):

    if "patient_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM doctors WHERE id=%s",
        (doctor_id,)
    )

    doctor = cursor.fetchone()

    if request.method == "POST":

        date = request.form["date"]
        time = request.form["time"]

        cursor.execute(
            """
            SELECT * FROM appointments
            WHERE doctor_id=%s
            AND appointment_date=%s
            AND appointment_time=%s
            """,
            (doctor_id, date, time)
        )

        existing = cursor.fetchone()

        if existing:

            flash(
                "This appointment slot is already booked.",
                "danger"
            )

        else:

            cursor.execute(
                """
                INSERT INTO appointments
                (patient_id, doctor_id,
                appointment_date, appointment_time)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    session["patient_id"],
                    doctor_id,
                    date,
                    time
                )
            )

            db.commit()

            flash(
                "Appointment booked successfully!",
                "success"
            )

            cursor.close()
            db.close()

            return redirect(
                url_for("my_appointments")
            )

    cursor.close()
    db.close()

    return render_template(
        "appointment.html",
        doctor=doctor
    )


# ---------------- MY APPOINTMENTS ----------------

@app.route("/my-appointments")
def my_appointments():

    if "patient_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT
            appointments.*,
            doctors.name AS doctor_name,
            doctors.specialization,
            hospitals.name AS hospital_name

        FROM appointments

        JOIN doctors
        ON appointments.doctor_id = doctors.id

        JOIN hospitals
        ON doctors.hospital_id = hospitals.id

        WHERE appointments.patient_id=%s

        ORDER BY appointment_date DESC
        """,
        (session["patient_id"],)
    )

    appointments = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "my_appointments.html",
        appointments=appointments
    )


# ---------------- CANCEL ----------------

@app.route("/cancel/<int:appointment_id>")
def cancel_appointment(appointment_id):

    if "patient_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE appointments
        SET status='Cancelled'
        WHERE id=%s
        AND patient_id=%s
        """,
        (
            appointment_id,
            session["patient_id"]
        )
    )

    db.commit()

    cursor.close()
    db.close()

    flash(
        "Appointment cancelled.",
        "success"
    )

    return redirect(
        url_for("my_appointments")
    )


# ---------------- AI ASSISTANT ----------------

@app.route("/ai-assistant")
def ai_assistant():

    if "patient_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "ai_assistant.html"
    )


@app.route("/api/ai-assistant", methods=["POST"])
def ai_assistant_api():

    data = request.get_json()

    message = data.get("message", "").lower()

    department = None

    if "heart" in message or "cardio" in message:
        department = "Cardiology"

    elif "eye" in message or "vision" in message:
        department = "Eye"

    elif "dental" in message or "tooth" in message:
        department = "Dental"

    elif "brain" in message or "neuro" in message:
        department = "Neurology"

    if department:

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            """
            SELECT
                doctors.id,
                doctors.name,
                doctors.specialization,
                hospitals.name AS hospital_name

            FROM doctors

            JOIN hospitals
            ON doctors.hospital_id = hospitals.id

            WHERE hospitals.department=%s
            """,
            (department,)
        )

        doctors = cursor.fetchall()

        cursor.close()
        db.close()

        return jsonify({
            "reply":
                f"I found doctors in {department}.",
            "doctors": doctors
        })

    return jsonify({
        "reply":
            "I can help you find Eye, Dental, Cardiology or Neurology doctors. Please tell me your requirement.",
        "doctors": []
    })


if __name__ == "__main__":
    app.run(debug=True)
