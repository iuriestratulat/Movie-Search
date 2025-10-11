from local_settings import MONGODB_URL_WRITE
from pymongo import MongoClient, errors
import sql_connector  # Used to map genre IDs to names for search_frequency_genre()

# MongoDB configuration
COLLECTION_NAME = 'final_project_030325_Iurie_Stratulat'
DB_NAME = 'ich_edit'


# ------------ Helper: get MongoDB collection ------------ #
def get_collection():
    """Connect to MongoDB and return the configured collection."""
    try:
        client = MongoClient(MONGODB_URL_WRITE)
        return client[DB_NAME][COLLECTION_NAME]
    except errors.ConnectionFailure as e:
        print("MongoDB connection error:", e)
        return None


# ------------ Helper: run aggregation ------------ #
def run_aggregation(pipeline):
    """
    Run a MongoDB aggregation pipeline on the configured collection.
    Returns a list of results, or an empty list in case of error.
    """
    try:
        collection = get_collection()
        if collection is None:  # FIX: verificare explicită
            return []
        return list(collection.aggregate(pipeline))
    except errors.PyMongoError as e:
        print("MongoDB aggregation error:", e)
        return []
    except Exception as e:
        print("Unexpected error during aggregation:", e)
        return []


# ------------ Statistics: top 5 keyword searches ------------ #
def search_frequency_key_word():
    """Return top 5 most searched keywords."""
    pipeline = [
        {'$match': {'search_type': 'keyword'}},
        {'$group': {'_id': '$params.key_word', 'search_frequency': {'$sum': 1}}},
        {'$sort': {'search_frequency': -1}},
        {'$project': {'word': '$_id', '_id': 0, 'search_frequency': 1}},
        {'$limit': 5}
    ]
    return run_aggregation(pipeline)


# ------------ Statistics: top 5 year searches ------------ #
def search_frequency_year():
    """Return top 5 most searched years."""
    pipeline = [
        {'$match': {'search_type': 'by_year'}},
        {'$group': {'_id': '$params.year', 'search_frequency': {'$sum': 1}}},
        {'$sort': {'search_frequency': -1}},
        {'$project': {'year': '$_id', '_id': 0, 'search_frequency': 1}},
        {'$limit': 5}
    ]
    return run_aggregation(pipeline)


# ------------ Statistics: top 5 genres ------------ #
def search_frequency_genre():
    """
    Return the top 5 searched genres with their names from MySQL.
    Uses genre_id → genre_name mapping from MySQL.
    """
    genres = sql_connector.get_genres()
    genre_map = {str(g[0]): g[1] for g in genres}

    pipeline = [
        {'$match': {'search_type': 'genre'}},
        {'$group': {'_id': '$params.genre_id', 'search_frequency': {'$sum': 1}}},
        {'$sort': {'search_frequency': -1}},
        {'$limit': 5}
    ]

    raw_results = run_aggregation(pipeline)

    return [
        {
            'genre_name': genre_map.get(str(entry['_id']), f"Unknown (ID {entry['_id']})"),
            'search_frequency': entry['search_frequency']
        }
        for entry in raw_results
    ]


# ------------ Statistics: top 5 year intervals ------------ #
def search_frequency_interval():
    """Return top 5 most searched year intervals, grouped into decades."""
    pipeline = [
        {'$match': {'search_type': 'years_interval'}},
        {'$addFields': {
            'year_start': {'$toInt': {'$arrayElemAt': ['$params.firstyear', 0]}},
            'year_end': {'$toInt': {'$arrayElemAt': ['$params.secondyear', 0]}}
        }},
        {'$addFields': {
            'midpoint_year': {
                '$floor': {
                    '$divide': [{'$add': ['$year_start', '$year_end']}, 2]
                }
            }
        }},
        {'$bucket': {
            'groupBy': '$midpoint_year',
            'boundaries': [1900, 1910, 1920, 1930, 1940, 1950, 1960,
                           1970, 1980, 1990, 2000, 2010, 2020, 2030],
            'default': 'Other',
            'output': {
                'search_frequency': {'$sum': 1},
                'examples': {'$push': {'start': '$year_start', 'end': '$year_end'}}
            }
        }},
        {'$sort': {'search_frequency': -1}},
        {'$project': {
            'decade_range': {
                '$concat': [
                    {'$toString': '$_id'},
                    '-',
                    {'$toString': {'$add': ['$_id', 9]}}
                ]
            },
            'search_frequency': 1,
            '_id': 0
        }},
        {'$limit': 5}
    ]
    return run_aggregation(pipeline)
