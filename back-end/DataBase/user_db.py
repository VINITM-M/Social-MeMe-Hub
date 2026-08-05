from DataBase.database import db_pool
import bcrypt

#password Implemention with bcrypt function 
def hash_password(plain_password):
    # Convert the password to bytes
    pw_bytes = plain_password.encode('utf-8')
    # Generate salt with cost factor 12
    salt = bcrypt.gensalt(rounds=12)
    # Hash the password
    hashed = bcrypt.hashpw(pw_bytes, salt)
    return hashed

def verify_password(plain_password, hashed):
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(plain_password, hashed)

def get_user_by_email(email):
    conn = db_pool.get_connection() 
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM USERS WHERE email=%s",
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
            """,(email, hashed_pw)
        )

        conn.commit()
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