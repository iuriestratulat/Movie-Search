from local_settings import MONGODB_URL_WRITE
from pymongo import MongoClient, errors
from datetime import datetime

# MongoDB configuration
GROUP_ID = "030325"
FULL_NAME = "Iurie_Stratulat"
DB_NAME = "ich_edit"
COLLECTION_NAME = f"final_project_{GROUP_ID}_{FULL_NAME}"

client = None
collection = None


# ------------ Initialize MongoDB connection ------------ #
def init_mongo_connection():
    """Initialize MongoDB connection and return the collection object."""
    global client, collection
    try:
        client = MongoClient(MONGODB_URL_WRITE, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")  # Check connection immediately
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        print("MongoDB connection successful.")
    except errors.ServerSelectionTimeoutError as err:
        print("MongoDB connection failed:", err)
        client = None
        collection = None
    except Exception as e:
        print("Unexpected error connecting to MongoDB:", e)
        client = None
        collection = None


# Run initialization at import
init_mongo_connection()


# ------------ Log a search query ------------ #
def log_query(search_type, params, results_count):
    """
    Log a search query in MongoDB.

    :param search_type: str - type of search performed ("keyword", "by_year", "genre", etc.)
    :param params: dict - parameters used for the search
    :param results_count: int - number of results found
    :return: bool - True if successfully logged, False otherwise
    """
    if collection is None:
        print("Cannot log — no MongoDB connection.")
        return False

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "search_type": search_type,
        "params": params,
        "results_count": results_count
    }

    try:
        collection.insert_one(log_entry)
        print("Log successfully written to MongoDB.")
        return True
    except errors.PyMongoError as e:
        print("MongoDB write error:", e)
        return False
    except Exception as e:
        print("Unexpected error while writing log:", e)
        return False


# ------------ Close MongoDB connection ------------ #
def close_mongo():
    """Close the MongoDB connection if open."""
    global client
    if client:
        try:
            client.close()
            print("MongoDB connection closed.")
        except Exception as e:
            print("Error closing MongoDB connection:", e)
        client = None
