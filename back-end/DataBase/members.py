from DataBase.database import db_pool 
<<<<<<< HEAD
def add_host(room_id, user_id):
    return add_member(room_id, user_id, role='host')
=======

def add_host(room_id, user_id):
    return add_member(room_id, user_id, role='host')

>>>>>>> fd6ff0a37a3386bff42393694047fd1e4a63bb16
def add_player(room_id, user_id):
    return add_member(room_id, user_id, role='player')

def add_member(room_id, user_id, role):
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            INSERT INTO room_members (room_id, user_id, role, status)
            VALUES (%s, %s, %s, 'Active')
            """,
            (room_id, str(user_id), role)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def is_member(room_id, user_id):
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT * FROM room_members
            WHERE room_id = %s AND user_id = %s
            """,
            (room_id, str(user_id))
        )
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        conn.close()

def count_members(room_id):
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT COUNT(*) AS cnt FROM room_members
            WHERE room_id = %s
            """,
            (room_id,)
        )
        row = cursor.fetchone()
        return row['cnt'] if row else 0
    finally:
        cursor.close()
        conn.close()