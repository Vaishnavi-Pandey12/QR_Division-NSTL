import os
from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config.settings import Config
from database.mongo import init_db
from services.auth_service import AuthService
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.api import api_bp

login_manager = LoginManager()
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    return AuthService.get_user_by_id(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    init_db(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
