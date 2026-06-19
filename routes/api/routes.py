from flask import Blueprint, jsonify
from utils.decorators import login_required
from services.document_service import DocumentService

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.get('/dashboard/charts')
@login_required
def dashboard_charts():
    return jsonify(DocumentService.chart_data())
