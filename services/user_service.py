from datetime import datetime, timezone
from bson import ObjectId
from werkzeug.security import generate_password_hash
from database.mongo import get_db
from services.auth_service import VALID_ROLES


class UserService:
    @staticmethod
    def list_users():
        return list(get_db().users.find().sort("created_at", -1))

    @staticmethod
    def find_user(user_id):
        return get_db().users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def update_user(user_id, payload):
        if "role" in payload and payload["role"] not in VALID_ROLES:
            payload["role"] = "user"
        if "email" in payload:
            payload["email"] = payload["email"].strip().lower()
        payload["updated_at"] = datetime.now(timezone.utc)
        return get_db().users.update_one({"_id": ObjectId(user_id)}, {"$set": payload})

    @staticmethod
    def deactivate_user(user_id):
        return UserService.update_user(user_id, {"is_active": False})

    @staticmethod
    def activate_user(user_id):
        return UserService.update_user(user_id, {"is_active": True})

    @staticmethod
    def reset_password(user_id, password):
        return UserService.update_user(
            user_id, {"password": generate_password_hash(password)}
        )
