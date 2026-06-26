from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from services.auth_service import AuthService, VALID_ROLES
from services.user_service import UserService
from services.document_service import DocumentService
from services.report_service import ReportService
from services.activity_service import ActivityService
from utils.decorators import admin_required, manager_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        stats=DocumentService.dashboard_stats(),
        recent=ActivityService.recent(),
        name=current_user.name,
    )


@admin_bp.route("/users")
@admin_required
def users():
    return render_template(
        "admin/users.html", users=UserService.list_users(), roles=sorted(VALID_ROLES)
    )


@admin_bp.route("/users/create", methods=["GET", "POST"])
@admin_required
def create_user():
    if request.method == "POST":
        AuthService.create_user(
            request.form["name"],
            request.form["email"],
            request.form.get("phone", ""),
            request.form["password"],
            request.form.get("role", "user"),
            True,
        )
        ActivityService.log(current_user, "User Creation", request.form["email"])
        flash("User created.", "success")
        return redirect(url_for("admin.users"))
    return render_template("admin/user_form.html", user=None, roles=sorted(VALID_ROLES))


@admin_bp.route("/users/<user_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    user = UserService.find_user(user_id)
    if request.method == "POST":
        UserService.update_user(
            user_id,
            {
                "name": request.form["name"],
                "email": request.form["email"],
                "phone": request.form.get("phone", ""),
                "role": request.form.get("role", "user"),
                "is_active": request.form.get("is_active") == "on",
            },
        )
        ActivityService.log(current_user, "Edit User", request.form["email"])
        flash("User updated.", "success")
        return redirect(url_for("admin.users"))
    return render_template("admin/user_form.html", user=user, roles=sorted(VALID_ROLES))


@admin_bp.post("/users/<user_id>/deactivate")
@admin_required
def deactivate_user(user_id):
    UserService.deactivate_user(user_id)
    ActivityService.log(current_user, "Deactivate User", user_id)
    flash("User deactivated.", "warning")
    return redirect(url_for("admin.users"))


@admin_bp.post("/users/<user_id>/activate")
@admin_required
def activate_user(user_id):
    UserService.activate_user(user_id)
    ActivityService.log(current_user, "Activate User", user_id)
    flash("User activated.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.post("/users/<user_id>/reset-password")
@admin_required
def reset_password(user_id):
    UserService.reset_password(user_id, request.form["password"])
    ActivityService.log(current_user, "Reset Password", user_id)
    flash("Password reset.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/upload", methods=["GET", "POST"])
@manager_required
def upload():
    if request.method == "POST":
        saved = DocumentService.save_upload(request.files.get("document"))
        if not saved:
            flash("Please upload a supported file: PDF, DOCX, XLSX, or PPTX.", "danger")
            return redirect(url_for("admin.upload"))
        result = DocumentService.create_document(request.form, saved, current_user)
        ActivityService.log(
            current_user, "Upload", request.form.get("title", str(result.inserted_id))
        )
        flash("Document uploaded.", "success")
        return redirect(url_for("admin.upload"))
    return render_template(
        "admin/upload.html",
        report_types=ReportService.list_report_types(),
        # investigation_types=ReportService.list_investigation_types(),
        # clients=ReportService.list_clients()
    )


@admin_bp.route("/report-types", methods=["GET", "POST"])
@admin_required
def report_types():
    if request.method == "POST":
        ReportService.create_report_type(
            request.form["name"],
            request.form.get("sub_type", ""),
            request.form.get("description", ""),
        )
        ActivityService.log(current_user, "Create Report Type", request.form["name"])
        flash("Report type created.", "success")
        return redirect(url_for("admin.report_types"))
    return render_template(
        "admin/settings.html", report_types=ReportService.list_report_types()
    )


@admin_bp.route("/report-types/<report_type_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_report_type(report_type_id):
    if request.method == "POST":

        ReportService.update_report_type(
            report_type_id,
            {
                "name": request.form["name"].strip(),
                "sub_type": request.form.get("sub_type", "").strip(),
                "description": request.form.get("description", "").strip(),
            },
        )

        ActivityService.log(
            current_user,
            "Edit Report Type",
            request.form["name"]
        )

        flash("Report type updated.", "success")
        return redirect(url_for("admin.report_types"))

    return render_template(
        "admin/settings.html",
        report_types=ReportService.list_report_types(),
        edit_type=ReportService.get_report_type(report_type_id),
    )


@admin_bp.post("/report-types/<report_type_id>/delete")
@admin_required
def delete_report_type(report_type_id):
    ReportService.delete_report_type(report_type_id)
    ActivityService.log(current_user, "Delete Report Type", report_type_id)
    flash("Report type deleted.", "warning")
    return redirect(url_for("admin.report_types"))


@admin_bp.route("/settings")
@admin_required
def settings():
    return redirect(url_for("admin.report_types"))
