import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/qr_division_nstl")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "qr_division_nstl")
    
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    ALLOWED_EXTENSIONS = {"pdf", "docx", "xlsx", "pptx"}
