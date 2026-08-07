import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager

db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    host="localhost",
    database="rooms",
    user="root",
    password="Vinith@2507,."
)
#connection pooling 

@contextmanager
def get_db():
    conn = None
    cursor = None
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        yield conn, cursor
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass