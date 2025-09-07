from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.auth_utils import verify_admin

auth_bp = Blueprint("auth", __name__)

# =============== LOGIN ROUTES ===============

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        success, msg = verify_admin(username, password)
        if success:
            session["admin"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard.dashboard_home"))
        else:
            flash(msg, "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("admin", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))
