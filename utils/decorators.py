from functools import wraps
from flask import abort, redirect, url_for, request
from flask_login import current_user

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.full_path))
        return fn(*args, **kwargs)
    return wrapper

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login', next=request.full_path))
            if getattr(current_user, 'role', None) not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(fn):
    return role_required('admin')(fn)

def manager_required(fn):
    return role_required('admin', 'manager')(fn)
