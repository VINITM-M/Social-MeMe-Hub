from DataBase.database import db_pool 

def init_db():
    conn = db_pool.get_connection() 
    cursor = conn.cursor() 

    try:

        # USERS Table 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        );
<<<<<<< HEAD
        """) 
=======
        """)
>>>>>>> fd6ff0a37a3386bff42393694047fd1e4a63bb16

        # USERS Address Table 
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_address (
                    first_name VARCHAR(255) NOT NULL, 
                    last_name VARCHAR(255) NOT NULL, 
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
            email VARCHAR(255) NOT NULL,
            role ENUM('host', 'player') DEFAULT 'player', 
            ready BOOLEAN DEFAULT FALSE, 
            status VARCHAR(50) DEFAULT 'active',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            UNIQUE(room_id), 
            FOREIGN KEY(room_id) REFERENCES rooms(room_id) ON DELETE CASCADE, 
            FOREIGN KEY(email) REFERENCES users(email) ON DELETE CASCADE
        );
        """)

<<<<<<< HEAD
        #OTP Expiration Table 
        cursor.execute("""
        CREATE TABLE email_otps (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            otp_hash VARCHAR(255) NOT NULL,
            expires_at DATETIME NOT NULL,
            attempts INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        

=======
>>>>>>> fd6ff0a37a3386bff42393694047fd1e4a63bb16
        conn.commit()
        print("Database schema initialized successfully.")
    except Exception as e:
        print("Schema initialization warning:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()