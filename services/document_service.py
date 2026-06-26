from fileinput import filename
import os
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from flask import current_app
from database.mongo import get_db, get_fs
from bson import ObjectId
import gridfs
from flask import Response
from flask import send_file



class DocumentService:
    @staticmethod
    def allowed_file(filename):
        return bool(
            filename
            and "." in filename
            and filename.rsplit(".", 1)[1].lower()
            in current_app.config["ALLOWED_EXTENSIONS"]
        )

    @staticmethod
    def save_upload(file_storage):
        if not file_storage or not DocumentService.allowed_file(file_storage.filename):
            return None

        filename = (
            f"{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}_"
            f"{secure_filename(file_storage.filename)}"
        )

        fs = get_fs()

        file_id = fs.put(
            file_storage.stream,
            filename=filename,
            content_type=file_storage.content_type,
        )

        return filename, file_id

    @staticmethod
    def create_document(form, saved_file, user):
        now = datetime.now(timezone.utc)
        data = {key: (form.get(key) or "").strip() for key in form.keys()}
        report_date = data.get("report_date")
        if report_date:
            data["year"] = report_date[:4]
            
        filename, file_id = saved_file if saved_file else ("", None)
        data.update(
            {
                "file_name": filename,
                "file_id": file_id,
                "uploaded_by": user.id,
                "created_by": user.id,
                "created_by_name": user.name,
                "author_email": data.get("author_email", "").lower(),
                "status": "Pending",
                "created_at": now,
            }
        )
        return get_db().documents.insert_one(data)
    
    @staticmethod
    def get_document(document_id):
        db = get_db()

        return db.documents.find_one({
            "_id": ObjectId(document_id)
        })
    
    @staticmethod
    def view_pdf(document_id):

        db = get_db()

        document = db.documents.find_one({
            "_id": ObjectId(document_id)
        })

        fs = gridfs.GridFS(db)
        print(document)
        print(type(document["file_id"]))
        print(document["file_id"])
        pdf = fs.get(ObjectId(document["file_id"]))
        print(pdf.filename)
        print(pdf.content_type)
        print(pdf.length)
        return Response(
            pdf.read(),
            mimetype="application/pdf",
            headers={
                "Content-Disposition":
                "inline; filename=report.pdf"
            }
        )
    
    @staticmethod
    def download_pdf(document_id):

        db = get_db()

        document = db.documents.find_one({
            "_id": ObjectId(document_id)
        })

        fs = gridfs.GridFS(db)

        pdf = fs.get(ObjectId(document["file_id"]))

        return Response(
            pdf.read(),
            mimetype="application/pdf",
            headers={
                "Content-Disposition":
                f'attachment; filename="{document["title"]}.pdf"'
            }
        )

    @staticmethod
    def dashboard_stats():
        db = get_db()
        now = datetime.now(timezone.utc)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return {
            "total_documents": db.documents.count_documents({}),
            "total_users": db.users.count_documents({}),
            "users": db.users.count_documents({}),
            "pending_approvals": db.documents.count_documents({"status": "Pending"}),
            "uploads_this_month": db.documents.count_documents(
                {"created_at": {"$gte": month_start}}
            ),
        }

    @staticmethod
    def search(filters, page=1, per_page=20, sort="created_at", direction="desc"):
        query = {}
        for field in [
            "title",
            "document_number",
            "author",
            "year",
            "division",
            "report_type",
            "investigation_type",
            "client",
            "platform_type",
        ]:
            value = filters.get(field)
            if value:
                query[field] = {"$regex": value, "$options": "i"}
        if filters.get("content"):
            query["$text"] = {"$search": filters["content"]}
        safe_sort = (
            sort
            if sort
            in [
                "title",
                "document_number",
                "author",
                "year",
                "division",
                "report_type",
                "created_at",
            ]
            else "created_at"
        )
        order = -1 if direction == "desc" else 1
        skip = max(page - 1, 0) * per_page
        cursor = (
            get_db()
            .documents.find(query)
            .sort(safe_sort, order)
            .skip(skip)
            .limit(per_page)
        )
        return list(cursor), get_db().documents.count_documents(query)

    @staticmethod
    def chart_data():
        db = get_db()
        monthly = list(
            db.documents.aggregate(
                [
                    {
                        "$group": {
                            "_id": {
                                "$dateToString": {
                                    "format": "%Y-%m",
                                    "date": "$created_at",
                                }
                            },
                            "count": {"$sum": 1},
                        }
                    },
                    {"$sort": {"_id": 1}},
                    {"$limit": 12},
                ]
            )
        )
        by_type = list(
            db.documents.aggregate(
                [
                    {"$group": {"_id": "$report_type", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                    {"$limit": 10},
                ]
            )
        )
        by_division = list(
            db.documents.aggregate(
                [
                    {"$group": {"_id": "$division", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                    {"$limit": 10},
                ]
            )
        )
        return {
            "uploads_per_month": {
                "labels": [m["_id"] or "Unknown" for m in monthly],
                "data": [m["count"] for m in monthly],
            },
            "report_distribution": {
                "labels": [r["_id"] or "Unknown" for r in by_type],
                "data": [r["count"] for r in by_type],
            },
            "documents_by_division": {
                "labels": [d["_id"] or "Unknown" for d in by_division],
                "data": [d["count"] for d in by_division],
            },
        }
