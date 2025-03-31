import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from werkzeug.security import generate_password_hash, check_password_hash

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)
    
    # Create eye_tests table linked to users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eye_tests (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        right_eye_snellen VARCHAR(10),
        left_eye_snellen VARCHAR(10),
        right_eye_duochrome VARCHAR(20),
        left_eye_duochrome VARCHAR(20),
        result TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def register_user(username, email, password):
    """Registers a new user with hashed password."""
    password_hash = generate_password_hash(password)
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s) RETURNING id;
        """, (username, email, password_hash))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id
    except psycopg2.IntegrityError:
        conn.rollback()
        return None  # Username or email already exists
    finally:
        cursor.close()
        conn.close()

def validate_user(username, password):
    """Validates user login."""
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE username = %s;", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        return user  # Return user data if login is valid
    return None

def get_user_by_id(user_id):
    """Fetch user details by ID."""
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, username, email FROM users WHERE id = %s;", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def save_test_result(user_id, right_eye, left_eye, right_duochrome, left_duochrome, result):
    """Saves an eye test result linked to a user."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO eye_tests (user_id, right_eye_snellen, left_eye_snellen, right_eye_duochrome, left_eye_duochrome, result)
    VALUES (%s, %s, %s, %s, %s, %s);
    """, (user_id, right_eye, left_eye, right_duochrome, left_duochrome, result))
    conn.commit()
    cursor.close()
    conn.close()

def get_results(user_id):
    """Fetch all test results for a specific user."""
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM eye_tests WHERE user_id = %s ORDER BY timestamp DESC;", (user_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

if __name__ == "__main__":
    create_tables()
    print("Database initialized and tables created!")