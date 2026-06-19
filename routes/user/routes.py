from flask import Blueprint, render_template, request
from flask_login import current_user
from services.document_service import DocumentService
from utils.decorators import login_required

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("user/dashboard.html", stats=DocumentService.dashboard_stats(), recent=DocumentService.recent_activity(), name=current_user.name)

@user_bp.route("/search")
@login_required
def search():
    return render_template("user/search.html", results=DocumentService.search(request.args), filters=request.args)

@user_bp.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html", user=current_user)
