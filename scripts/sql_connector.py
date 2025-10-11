import pymysql
from local_settings import dbconfig

# --- Helper Function to get a new connection ---
def _get_connection():
    """Creates and returns a new database connection."""
    try:
        return pymysql.connect(**dbconfig)
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None

# --- Keyword Search ---
def find_by_key_word(key_word, offset=0):
    """
    Returns movies where the title or description contains the keyword.
    This search is case-insensitive.
    """
    sql = """
        SELECT film_id, title, description, release_year
        FROM film
        WHERE LOWER(title) LIKE LOWER(%s) OR LOWER(description) LIKE LOWER(%s)
        ORDER BY title
        LIMIT 10 OFFSET %s
    """
    connection = _get_connection()
    if not connection:
        return []
    try:
        with connection.cursor() as cursor:
            search_term = f"%{key_word}%"
            cursor.execute(sql, (search_term, search_term, offset))
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"SQL error in find_by_key_word: {e}")
        return []
    finally:
        if connection:
            connection.close()

# --- Year / Year Interval Search ---
def get_min_year():
    sql = "SELECT MIN(release_year) FROM film;"
    connection = _get_connection()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0] if result else None
    except pymysql.MySQLError as e:
        print(f"SQL error in get_min_year: {e}")
        return None
    finally:
        if connection:
            connection.close()

def get_max_year():
    sql = "SELECT MAX(release_year) FROM film;"
    connection = _get_connection()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0] if result else None
    except pymysql.MySQLError as e:
        print(f"SQL error in get_max_year: {e}")
        return None
    finally:
        if connection:
            connection.close()

def get_films_by_year(year, offset=0):
    sql = """
        SELECT film_id, title, description, release_year
        FROM film
        WHERE release_year = %s
        ORDER BY title
        LIMIT 10 OFFSET %s
    """
    connection = _get_connection()
    if not connection:
        return False, []
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (year, offset))
            return True, cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"SQL error in get_films_by_year: {e}")
        return False, []
    finally:
        if connection:
            connection.close()

def get_films_by_years_interval(first_year, second_year, offset=0):
    sql = """
        SELECT film_id, title, description, release_year
        FROM film
        WHERE release_year BETWEEN %s AND %s
        ORDER BY release_year, title
        LIMIT 10 OFFSET %s
    """
    connection = _get_connection()
    if not connection:
        return False, []
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (first_year, second_year, offset))
            return True, cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"SQL error in get_films_by_years_interval: {e}")
        return False, []
    finally:
        if connection:
            connection.close()

# --- Genre Search ---
def get_genres():
    sql = "SELECT category_id, name FROM category ORDER BY name;"
    connection = _get_connection()
    if not connection:
        return []
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"SQL error in get_genres: {e}")
        return []
    finally:
        if connection:
            connection.close()

def find_films_by_genres(genre_id, offset=0):
    sql = """
        SELECT f.title, f.description, f.release_year
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        WHERE fc.category_id = %s
        ORDER BY f.title
        LIMIT 10 OFFSET %s
    """
    connection = _get_connection()
    if not connection:
        return False, []
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (genre_id, offset))
            return True, cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"SQL error in find_films_by_genres: {e}")
        return False, []
    finally:
        if connection:
            connection.close()
