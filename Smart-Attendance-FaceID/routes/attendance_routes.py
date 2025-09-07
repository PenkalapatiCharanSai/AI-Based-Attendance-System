from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.face_utils import capture_face_from_webcam, recognize_and_mark_attendance
from models.user_model import register_user

attendance_bp = Blueprint("attendance", __name__)

# =============== REGISTER STUDENT ===============

@attendance_bp.route("/register", methods=["GET", "POST"])
def register_student():
    if "admin" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        student_id = request.form.get("student_id")
        name = request.form.get("name")
        year = request.form.get("year")
        department = request.form.get("department")

        # Capture face using webcam
        face_encoding = capture_face_from_webcam()
        if face_encoding is None:
            flash("No face captured. Try again.", "danger")
            return redirect(url_for("attendance.register_student"))

        success, msg = register_user(student_id, name, year, department, face_encoding)
        flash(msg, "success" if success else "danger")
        return redirect(url_for("dashboard.dashboard_home"))

    return render_template("register.html")


# =============== ATTENDANCE MARKING ===============

@attendance_bp.route("/attendance")
def take_attendance():
    if "admin" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    recognize_and_mark_attendance()
    flash("Attendance session completed.", "info")
    return redirect(url_for("dashboard.dashboard_home"))
