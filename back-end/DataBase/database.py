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