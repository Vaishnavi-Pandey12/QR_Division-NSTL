from flask import Blueprint, render_template, request
from flask_login import current_user
from services.document_service import DocumentService
from services.activity_service import ActivityService
from services.report_service import ReportService
from utils.decorators import login_required
from database.mongo import get_db

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "user/dashboard.html",
        stats=DocumentService.dashboard_stats(),
        recent=ActivityService.recent(),
        name=current_user.name,
    )


@user_bp.route("/search")
@login_required
def search():
    page = request.args.get("page", 1, type=int)
    results, total = DocumentService.search(
        request.args,
        page=page,
        sort=request.args.get("sort", "created_at"),
        direction=request.args.get("direction", "desc"),
    )
    if request.args:
        ActivityService.log(
            current_user,
            "Search",
            ", ".join(f"{k}={v}" for k, v in request.args.items() if v),
        )
    return render_template(
        "user/search.html",
        results=results,
        filters=request.args,
        page=page,
        total=total,
        report_types=sorted(
            [rt for rt in get_db().documents.distinct("report_type") if rt]
        ),
    )


@user_bp.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html", user=current_user)
