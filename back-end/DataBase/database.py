import mysql.connector
from mysql.connector import pooling

db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    host="localhost",
    database="rooms",
    user="root",
    password="Vinith@2507,."
)
#connection pooling 

def get_db():
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        yield conn, cursor
    finally:
        cursor.close()
        conn.close()