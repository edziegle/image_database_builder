from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

COLLECTIONS = ["image_directories", "images"]


def get_db_client() -> MongoClient:
    """
    Returns a new MongoDB client.
    """
    return MongoClient()


def get_db(client: MongoClient, name: str = "image_database") -> Database:
    """
    Returns a MongoDB database.
    """
    return client[name]


def get_collection(db: Database, name: str) -> Collection:
    """
    Returns a MongoDB collection.
    """
    if name not in COLLECTIONS:
        raise ValueError(f"Collection {name} not found.")
    return db[name]
