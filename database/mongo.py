from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from flask import current_app
import gridfs

client = None
db = None
fs = None

def init_db(app):
    global client, db, fs

    client = MongoClient(app.config["MONGO_URI"])
    db = client[app.config["MONGO_DB_NAME"]]

    fs = gridfs.GridFS(db)

    create_indexes()
    return db

def get_fs():
    global fs

    if fs is None:
        database = get_db()
        return gridfs.GridFS(database)

    return fs


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
    database.documents.create_index(
        [
            ("title", TEXT),
            ("summary", TEXT),
            ("document_number", TEXT),
            ("author", TEXT),
        ]
    )
    for field in [
        "year",
        "division",
        "report_type",
        "investigation_type",
        "client",
        "platform_type",
        "created_at",
    ]:
        database.documents.create_index(
            [(field, ASCENDING if field != "created_at" else DESCENDING)]
        )
    database.report_types.create_index(
        [("name", ASCENDING), ("sub_type", ASCENDING)], unique=True
    )
    database.activity_logs.create_index([("timestamp", DESCENDING)])
