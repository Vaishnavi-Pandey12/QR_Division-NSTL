from datetime import datetime, timezone
from bson import ObjectId
from database.mongo import get_db

DEFAULT_REPORT_TYPES = [
    'Final Acceptance Report', 'Issue of Boarding Pass', 'Failure Analysis Board',
    'Inspection Report', 'Verification Report', 'Defect Report', 'Defect Investigation Report'
]

class ReportService:
    @staticmethod
    def ensure_defaults():
        db = get_db()
        for name in DEFAULT_REPORT_TYPES:
            db.report_types.update_one({'name': name, 'sub_type': ''}, {'$setOnInsert': {'name': name, 'sub_type': '', 'created_at': datetime.now(timezone.utc)}}, upsert=True)

    @staticmethod
    def list_report_types():
        ReportService.ensure_defaults()
        return list(get_db().report_types.find().sort('name', 1))

    @staticmethod
    def create_report_type(name, sub_type='', description=''):
        return get_db().report_types.insert_one({'name': name.strip(), 'sub_type': sub_type.strip(), 'description': description.strip(), 'created_at': datetime.now(timezone.utc)})

    @staticmethod
    def get_report_type(report_type_id):
        return get_db().report_types.find_one({'_id': ObjectId(report_type_id)})

    @staticmethod
    def update_report_type(report_type_id, payload):
        payload['updated_at'] = datetime.now(timezone.utc)
        return get_db().report_types.update_one({'_id': ObjectId(report_type_id)}, {'$set': payload})

    @staticmethod
    def delete_report_type(report_type_id):
        return get_db().report_types.delete_one({'_id': ObjectId(report_type_id)})
