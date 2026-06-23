from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, data):
        self.data = data or {}
        self.id = str(self.data.get("_id"))
        self.name = self.data.get("name", "User")
        self.email = self.data.get("email", "")
        self.phone = self.data.get("phone", "")
        self.role = self.data.get("role", "user")
        self.is_active_flag = self.data.get("is_active", True)

    @property
    def is_active(self):
        return bool(self.is_active_flag)

    @property
    def is_admin(self):
        return self.role == "admin"
