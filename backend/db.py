import os
from datetime import datetime
from pymongo import MongoClient

def get_mongo_uri():
    # 1) Kaggle secrets
    try:
        from kaggle_secrets import UserSecretsClient
        user_secrets = UserSecretsClient()
        uri = user_secrets.get_secret("MONGO_URI")
        if uri and uri.strip():
            print(" Loaded MONGO_URI from Kaggle Secrets")
            return uri.strip()
    except Exception as e:
        print("Kaggle secret missing. Will try env var.")
        print("Reason:", str(e))

    # 2) Local env
    uri = os.getenv("MONGO_URI", "")
    if uri and uri.strip():
        print("Loaded MONGO_URI from environment")
        return uri.strip()

    print("No MONGO_URI found - DB logging disabled.")
    return None


MONGO_URI = get_mongo_uri()

client = MongoClient(MONGO_URI) if MONGO_URI else None

DB_NAME = os.getenv("DB_NAME", "nextyou_rag")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "query_logs")

collection = None
if client:
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]


def log_query(query, retrieved_chunks, answer, is_unsafe, safety_reason=None):
    if collection is None:
        return  # no DB logging

    collection.insert_one({
        "query": query,
        "retrieved_chunks": retrieved_chunks,
        "answer": answer,
        "isUnsafe": is_unsafe,
        "safety_reason": safety_reason,
        "timestamp": datetime.utcnow()
    })
