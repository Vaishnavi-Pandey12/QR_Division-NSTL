from flask import Blueprint, jsonify
from utils.decorators import login_required

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.get("/dashboard/charts")
@login_required
def dashboard_charts():
    return jsonify({
        "uploads_per_month": {"labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "data": [3, 7, 4, 8, 6, 10]},
        "documents_by_division": {"labels": ["QR", "NSTL", "HR", "Analysis"], "data": [12, 9, 5, 7]},
        "report_distribution": {"labels": ["Technical", "Investigation", "Trial", "Research"], "data": [10, 6, 4, 8]},
    })
