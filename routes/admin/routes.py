from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from services.auth_service import AuthService
from services.user_service import UserService
from services.document_service import DocumentService
from database.mongo import get_db
from utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    return render_template("admin/dashboard.html", stats=DocumentService.dashboard_stats(), recent=DocumentService.recent_activity(), name=current_user.name)

@admin_bp.route("/users")
@admin_required
def users():
    return render_template("admin/users.html", users=UserService.list_users())

@admin_bp.route("/users/create", methods=["GET", "POST"])
@admin_required
def create_user():
    if request.method == "POST":
        AuthService.create_user(request.form["name"], request.form["email"], request.form.get("phone", ""), request.form["password"], request.form.get("role", "user"), True)
        flash("User created.", "success")
        return redirect(url_for("admin.users"))
    return render_template("admin/user_form.html", user=None)

@admin_bp.route("/users/<user_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    user = UserService.find_user(user_id)
    if request.method == "POST":
        UserService.update_user(user_id, {"name": request.form["name"], "email": request.form["email"].lower(), "phone": request.form.get("phone", ""), "role": request.form.get("role", "user"), "is_active": request.form.get("is_active") == "on"})
        flash("User updated.", "success")
        return redirect(url_for("admin.users"))
    return render_template("admin/user_form.html", user=user)

@admin_bp.post("/users/<user_id>/disable")
@admin_required
def disable_user(user_id):
    UserService.disable_user(user_id); flash("User disabled.", "warning"); return redirect(url_for("admin.users"))

@admin_bp.post("/users/<user_id>/reset-password")
@admin_required
def reset_password(user_id):
    UserService.reset_password(user_id, request.form["password"]); flash("Password reset.", "success"); return redirect(url_for("admin.users"))

@admin_bp.route("/upload", methods=["GET", "POST"])
@admin_required
def upload():
    if request.method == "POST":
        file_path = DocumentService.save_upload(request.files.get("document"))
        DocumentService.create_document(request.form, file_path, current_user)
        flash("Document uploaded.", "success")
        return redirect(url_for("admin.upload"))
    return render_template("admin/upload.html")

@admin_bp.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    db = get_db()
    if request.method == "POST":
        db.report_types.insert_one({"name": request.form["name"], "sub_type": request.form.get("sub_type", ""), "description": request.form.get("description", "")})
        flash("Report type created.", "success")
        return redirect(url_for("admin.settings"))
    return render_template("admin/settings.html", report_types=list(db.report_types.find()))
