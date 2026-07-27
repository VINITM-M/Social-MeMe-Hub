from DataBase.database import db_pool

def get_user_by_email(email):
    conn = db_pool.get_connection() 
    cursor = conn.cursor(dictionary=True) 
    try:
        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        ) 
        user = cursor.fetchone() 
        return user
    finally:
        cursor.close() 
        conn.close() 


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


def create_user(user_id, user_name, email): 
    conn = db_pool.get_connection() 
    cursor = conn.cursor(dictionary=True) 
    try: 
        cursor.execute(
            """
            INSERT INTO users (user_id, user_name, email)
            VALUES (%s, %s, %s)
            """,
            (str(user_id), user_name, email)
        )  
        conn.commit() 
        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )
        return cursor.fetchone()
    except Exception as e: 
        print("Error creating user:", e)
        return get_user_by_email(email)
    finally: 
        cursor.close() 
        conn.close() 