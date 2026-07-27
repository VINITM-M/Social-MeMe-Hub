from DataBase.database import db_pool 

def init_db():
    conn = db_pool.get_connection() 
    cursor = conn.cursor() 

    try:

        # account-creation Table 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS account_creation (
            userName VARCHAR(255) NOT NULL, 
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # USERS Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT NOT NULL UNIQUE,
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
            UNIQUE(room_id), 
            FOREIGN KEY(room_id) REFERENCES rooms(room_id) ON DELETE CASCADE, 
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        conn.commit()
        print("Database schema initialized successfully.")
    except Exception as e:
        print("Schema initialization warning:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()