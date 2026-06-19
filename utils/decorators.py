from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        if getattr(current_user, "role", None) != "admin":
            abort(403)
        return fn(*args, **kwargs)
    return wrapper
