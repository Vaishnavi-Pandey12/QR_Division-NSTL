from flask import Blueprint, render_template, request, url_for
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
    per_page = request.args.get("per_page", 10, type=int)

    results, total = DocumentService.search(
        request.args,
        page=page,
        per_page=per_page,
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
        per_page=per_page,
        total_pages=(total + per_page - 1) // per_page,
        report_types=sorted(
            [rt for rt in get_db().documents.distinct("report_type") if rt]
        ),
    )


@user_bp.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html", user=current_user)

@user_bp.route("/document/<document_id>/view")
@login_required
def view_page(document_id):
    document = DocumentService.get_document(document_id)
    return render_template(
        "user/view_pdf.html",
        document=document
    )


@user_bp.route("/document/<document_id>/pdf")
@login_required
def view_pdf(document_id):
    return DocumentService.view_pdf(document_id)


@user_bp.route("/document/<document_id>")
@login_required
def document_details(document_id):
    document = DocumentService.get_document(document_id)

    return render_template(
        "user/document_details.html",
        document=document
    )

@user_bp.route("/document/<document_id>/viewer")
@login_required
def pdf_viewer(document_id):
    return render_template(
        "user/pdf_viewer.html",
        document_id=document_id
    )

@user_bp.route("/document/<document_id>/download")
@login_required
def download_pdf(document_id):

    return DocumentService.download_pdf(document_id)


@user_bp.route("/document/<document_id>/edit", methods=["GET", "POST"])
@login_required
def edit_document(document_id):

    document = DocumentService.get_document(document_id)

    if not document:
        flash("Document not found.", "danger")
        return redirect(url_for("user.search"))

    if request.method == "POST":

        DocumentService.update_document(
            document_id,
            request.form,
            request.files.get("document")
        )

        flash("Document updated successfully.", "success")

        return redirect(
            url_for(
                "user.document_details",
                document_id=document_id
            )
        )

    return render_template(
        "user/edit_document.html",
        document=document,
        report_types=ReportService.list_report_types()
    )


@user_bp.route("/document/<document_id>/delete", methods=["POST"])
@login_required
def delete_document(document_id):

    DocumentService.delete_document(document_id)

    flash("Document deleted successfully.", "success")

    return redirect(url_for("user.search"))