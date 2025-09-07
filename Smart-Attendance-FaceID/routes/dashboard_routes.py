from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
from models.user_model import get_all_users, get_all_attendance, get_attendance_by_date
from utils.csv_export import export_attendance_all, export_attendance_by_date
import datetime
import os

dashboard_bp = Blueprint("dashboard", __name__)

# =============== DASHBOARD HOME ===============

@dashboard_bp.route("/dashboard")
def dashboard_home():
    if "admin" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    today = datetime.date.today().strftime("%Y-%m-%d")
    attendance_today = get_attendance_by_date(today)
    students = get_all_users()

    stats = {
        "total_students": len(students),
        "present_today": len(attendance_today),
        "absent_today": len(students) - len(attendance_today)
    }

    return render_template("dashboard.html",
                           students=students,
                           attendance_today=attendance_today,
                           stats=stats)


# =============== EXPORT ATTENDANCE ===============

@dashboard_bp.route("/export/all")
def export_all():
    if "admin" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    success, msg = export_attendance_all()
    if success:
        return send_file("attendance_all.csv", as_attachment=True)
    else:
        flash(msg, "danger")
        return redirect(url_for("dashboard.dashboard_home"))


@dashboard_bp.route("/export/date", methods=["POST"])
def export_by_date():
    if "admin" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    date_str = request.form.get("date")
    success, msg = export_attendance_by_date(date_str)
    if success:
        filename = f"attendance_{date_str}.csv"
        return send_file(filename, as_attachment=True)
    else:
        flash(msg, "danger")
        return redirect(url_for("dashboard.dashboard_home"))
