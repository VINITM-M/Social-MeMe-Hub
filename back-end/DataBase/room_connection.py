import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool 

db_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host='localhost',
    database='postgres',
    user='postgres',
    password='Vinith@2507,.'
)

def add_user_details(user_name, email, user_id):
    conn = db_pool.getconn()

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            INSERT INTO users (user_name, email, user_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO NOTHING
            RETURNING *;
            """,
            (user_name, email, user_id)
        )
        row = cursor.fetchone()
        is_new = True

        if row is None:
            is_new = False
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cursor.fetchone()
        
        print("user Details Database: ", row)

        conn.commit()
        cursor.close()

    finally:
        db_pool.putconn(conn)

    return row, is_new

def save_room(room_id, room_code, room_name, capacity, rounds, region): 
    conn = db_pool.getconn()

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
                INSERT INTO rooms (room_id, room_code, room_name, capacity, rounds, region) 
                VALUES (%s, %s, %s, %s, %s, %s ) 
            """, 
            (
                room_id,
                room_code,
                room_name,
                capacity,
                rounds,
                region
             )
        )
        conn.commit()
        cursor.execute(
            "SELECT * FROM rooms WHERE room_id = %s", (room_id,)
        )
        rows = cursor.fetchone()
        print("Room Details Database: ", rows) 
        cursor.close()
    
    finally:
        db_pool.putconn(conn)

def add_host_to_room(room_id, user_id): 
    conn = db_pool.getconn() 

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
                INSERT INTO room_members (room_id, user_id, role, status) 
                VALUES (%s, %s, %s, %s) 
            """, 
            (room_id, user_id, "host", "active")
        )
        conn.commit()
        
        cursor.execute(
            "SELECT * FROM room_members WHERE room_id = %s AND user_id = %s", (room_id, user_id)
        )

        rows = cursor.fetchone()
        print("Room Members Database: ", rows) 
        cursor.close()

    finally:
        db_pool.putconn(conn)

def join_room(code, region, user_id):

    conn = db_pool.getconn()

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT room_id, room_code, room_name, capacity, rounds, region
            FROM rooms
            WHERE room_code = %s AND region = %s
            """,
            (code, region)
        )

        room = cursor.fetchone()
        print("fetched rows:", room)

        if room is None:
            return "Room not found"

        room_id = room['room_id']
        room_name = room['room_name']
        capacity = room['capacity']
        rounds = room['rounds']

        cursor.execute(
            """
            SELECT COUNT(*) AS cnt
            FROM room_members
            WHERE room_id = %s
            """,
            (room_id,)
        )

        result = cursor.fetchone()
        cnt = result['cnt']

        rem = capacity - cnt

        cursor.execute(
            """
            SELECT 1 FROM room_members
            WHERE user_id = %s
            """,
            (user_id,)
        )

        exists = cursor.fetchone()

        if exists:
            return {
                "status": "success",
                "message": "User already in room",
                "presentIn": cnt,
                "capacity": capacity,
                "room_id": room_id,
                "room_name": room_name,
                "rounds": rounds 
            }
        
        if rem > 0:
            cursor.execute(
                """
                INSERT INTO room_members (room_id, user_id, role, status)
                VALUES (%s, %s, %s, %s)
                """, 
                (room_id, user_id, 'player', 'active')
            )

            conn.commit()
            
            return {
                "status": "success",
                "message": "Joined successfully",
                "presentIn": cnt, 
                "capacity": capacity,
                "room_id": room_id, 
                "room_name": room_name,
                "rounds": rounds 
            }

        else:
            return {
            "status": "error",
            "message": "Room is full",
            "remaining_capacity": 0
        }

    finally:
        cursor.close()
        db_pool.putconn(conn)  