from pymongo import MongoClient, ASCENDING, DESCENDING
from flask import current_app

client = None
db = None

def init_db(app):
    global client, db
    client = MongoClient(app.config["MONGO_URI"])
    db = client[app.config["MONGO_DB_NAME"]]
    create_indexes()
    return db

def get_db():
    global db
    if db is None:
        client_local = MongoClient(current_app.config["MONGO_URI"])
        return client_local[current_app.config["MONGO_DB_NAME"]]
    return db

def create_indexes():
    database = get_db()
    database.users.create_index([("email", ASCENDING)], unique=True)
    database.users.create_index([("phone", ASCENDING)], sparse=True)
    database.users.create_index([("role", ASCENDING), ("is_active", ASCENDING)])
    database.documents.create_index([("title", "text"), ("content", "text"), ("document_number", "text"), ("author", "text")])
    database.documents.create_index([("created_at", DESCENDING)])
    database.report_types.create_index([("name", ASCENDING), ("sub_type", ASCENDING)], unique=True)
