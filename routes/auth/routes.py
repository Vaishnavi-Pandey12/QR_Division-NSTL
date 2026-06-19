from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user
from services.auth_service import AuthService
from services.activity_service import ActivityService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    return redirect(url_for("admin.dashboard" if current_user.role == "admin" else "user.dashboard"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))
    if request.method == "POST":
        user = AuthService.authenticate(request.form.get("identifier", ""), request.form.get("password", ""))
        if user:
            login_user(user)
            ActivityService.log(user, 'Login', 'Authentication')
            session["user_id"] = user.id
            session["name"] = user.name
            session["role"] = user.role
            return redirect(url_for("auth.index"))
        flash("Invalid credentials or disabled account.", "danger")
    return render_template("auth/login.html", admin_exists=AuthService.admin_exists())

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if AuthService.admin_exists():
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        if request.form.get("password") != request.form.get("confirm"):
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")
        try:
            AuthService.create_user(request.form["name"], request.form["email"], request.form.get("phone", ""), request.form["password"], role="admin")
            flash("First admin account created. Please log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception as exc:
            flash(f"Unable to create account: {exc}", "danger")
    return render_template("auth/register.html")

@auth_bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        ActivityService.log(current_user, 'Logout', 'Authentication')
    logout_user()
    session.clear()
    return redirect(url_for("auth.login"))
