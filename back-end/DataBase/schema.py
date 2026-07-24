from DataBase.database import db_pool 

def ensure_column(cursor, table_name, column_name, column_def):
    cursor.execute("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() 
          AND TABLE_NAME = %s 
          AND COLUMN_NAME = %s
    """, (table_name, column_name))
    res = cursor.fetchone()
    count = res[0] if res else 0
    if count == 0:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_def}")
        print(f"Added missing column '{column_name}' to table '{table_name}'.")

def init_db():
    conn = db_pool.get_connection() 
    cursor = conn.cursor() 

    try:
        # USERS Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(100) NOT NULL UNIQUE,
            user_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # ROOMS Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_id CHAR(36) PRIMARY KEY,
            room_code VARCHAR(10) NOT NULL,
            room_name VARCHAR(100) NOT NULL,
            host_id VARCHAR(100) NOT NULL,
            capacity INT NOT NULL,
            current_players INT DEFAULT 1,
            rounds INT,
            region VARCHAR(50),
            visibility ENUM('public','private') DEFAULT 'public',
            status ENUM('waiting','playing','finished') DEFAULT 'waiting',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # ROOM MEMBERS Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS room_members (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            room_id CHAR(36) NOT NULL,
            user_id VARCHAR(100) NOT NULL,
            role ENUM('host', 'player') DEFAULT 'player', 
            ready BOOLEAN DEFAULT FALSE, 
            status VARCHAR(50) DEFAULT 'active',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            UNIQUE(room_id, user_id), 
            FOREIGN KEY(room_id) REFERENCES rooms(room_id) ON DELETE CASCADE, 
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)
        
        # Ensure missing columns in existing tables are added if schema evolved
        ensure_column(cursor, "rooms", "host_id", "VARCHAR(100) NOT NULL DEFAULT ''")
        ensure_column(cursor, "rooms", "capacity", "INT NOT NULL DEFAULT 4")
        ensure_column(cursor, "rooms", "current_players", "INT DEFAULT 1")
        ensure_column(cursor, "rooms", "rounds", "INT DEFAULT 3")
        ensure_column(cursor, "rooms", "region", "VARCHAR(50)")
        ensure_column(cursor, "rooms", "visibility", "ENUM('public','private') DEFAULT 'public'")
        ensure_column(cursor, "rooms", "status", "ENUM('waiting','playing','finished') DEFAULT 'waiting'")

        ensure_column(cursor, "room_members", "role", "ENUM('host', 'player') DEFAULT 'player'")
        ensure_column(cursor, "room_members", "ready", "BOOLEAN DEFAULT FALSE")
        ensure_column(cursor, "room_members", "status", "VARCHAR(50) DEFAULT 'active'")

        conn.commit()
        print("Database schema initialized successfully.")
    except Exception as e:
        print("Schema initialization warning:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()