import os
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from flask import current_app
from database.mongo import get_db

class DocumentService:
    @staticmethod
    def allowed_file(filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

    @staticmethod
    def save_upload(file_storage):
        if not file_storage or not DocumentService.allowed_file(file_storage.filename):
            return None
        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
        filename = f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{secure_filename(file_storage.filename)}"
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file_storage.save(path)
        return f"uploads/{filename}"

    @staticmethod
    def create_document(form, file_path, user):
        data = {key: form.get(key) for key in form.keys()}
        data.update({"file_path": file_path, "status": "Pending", "created_by": user.id, "created_by_name": user.name,
                     "created_at": datetime.now(timezone.utc)})
        return get_db().documents.insert_one(data)

    @staticmethod
    def dashboard_stats():
        db = get_db()
        return {
            "total_documents": db.documents.count_documents({}),
            "pending_approvals": db.documents.count_documents({"status": "Pending"}),
            "users": db.users.count_documents({}),
            "uploads_this_month": db.documents.count_documents({}),
        }

    @staticmethod
    def recent_activity(limit=10):
        return list(get_db().activity.find().sort("date", -1).limit(limit))

    @staticmethod
    def search(filters):
        query = {}
        for field in ["title", "document_number", "author", "year", "division", "report_type", "investigation_type", "client", "platform_type"]:
            value = filters.get(field)
            if value:
                query[field] = {"$regex": value, "$options": "i"}
        if filters.get("content"):
            query["$text"] = {"$search": filters["content"]}
        return list(get_db().documents.find(query).sort("created_at", -1).limit(100))
