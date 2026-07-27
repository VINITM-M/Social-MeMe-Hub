from DataBase.database import db_pool 

def create_room(room_id, room_code, room_name, host_id, capacity, rounds, region): 

    conn = db_pool.get_connection() 
    cursor = conn.cursor(dictionary=True) 
    #inserting the data into existing room table 
    try: 
        cursor.execute(
            """
            INSERT INTO rooms (room_id, room_code, room_name, host_id, capacity, current_players, rounds, region)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (room_id, room_code, room_name, host_id, capacity, 1, rounds, region)  
        )
        conn.commit()

        cursor.execute(
            "SELECT * FROM rooms WHERE room_id = %s",
            (room_id,)
        )
        return cursor.fetchone()
    finally:
        cursor.close() 
        conn.close()

def get_room_by_code_and_region(room_code, region):
    #get the room by code and region 
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT * FROM rooms
            WHERE room_code = %s AND region = %s
            """,
            (room_code, region)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def increment_room_players(room_id):
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            UPDATE rooms
            SET current_players = current_players + 1
            WHERE room_id = %s
            """,
            (room_id,)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()
