from app.database.connection import db_pool, get_db
from app.algorithms.bloom_filter import DatabaseEmailBloomFilter
from app.security.hashing import hash_password

email_bloom_filter = DatabaseEmailBloomFilter()

def get_user_by_email(email):
    if not email_bloom_filter.might_contain(email):
        return None

    with get_db() as (conn, cursor):
        cursor.execute(
            """
            SELECT email, password FROM Users WHERE email=%s
            LIMIT 1
            """,
            (email,)
        )
        result = cursor.fetchone()
        return result


def find_user_by_email(email):
    """Use Bloom for the fast miss path, then verify with the real DB query."""
    if not email_bloom_filter.might_contain(email):
        return None

    with get_db() as (conn, cursor):
        cursor.execute(
            "SELECT email, password FROM Users WHERE email = %s LIMIT 1",
            (email,),
        )
        return cursor.fetchone()


def get_user_by_user_id(user_id):
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM users WHERE user_id=%s",
            (str(user_id),)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def create_user(first_name, last_name, email, password):
    hashed_pw = hash_password(password)
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            INSERT INTO users_address (
                first_name,
                last_name,
                email,
                created_at
            )
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            """,
            (first_name, last_name, email)
        )

        cursor.execute(
            """
            INSERT INTO users (email, password)
            VALUES (%s, %s)
            """,
            (email, hashed_pw)
        )

        conn.commit()
        email_bloom_filter.add(email)
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        return cursor.fetchone()

    except Exception as e:
        print("Error creating user:", e)
        return get_user_by_email(email)

    finally:
        cursor.close()
        conn.close()
