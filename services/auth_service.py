from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from database.mongo import get_db
from models.user import User

class AuthService:
    @staticmethod
    def admin_exists():
        return get_db().users.count_documents({"role": "admin"}) > 0

    @staticmethod
    def get_user_by_id(user_id):
        try:
            data = get_db().users.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None
        return User(data) if data else None

    @staticmethod
    def authenticate(identifier, password):
        data = get_db().users.find_one({"$or": [{"email": identifier.lower()}, {"phone": identifier}]})
        if not data or not data.get("is_active", True):
            return None
        if check_password_hash(data.get("password", ""), password):
            return User(data)
        return None

    @staticmethod
    def create_user(name, email, phone, password, role="user", is_active=True):
        doc = {
            "name": name.strip(), "email": email.strip().lower(), "phone": phone.strip(),
            "password": generate_password_hash(password), "role": role, "is_active": is_active,
        }
        result = get_db().users.insert_one(doc)
        doc["_id"] = result.inserted_id
        return User(doc)
