import sqlite3
import hashlib


DB_NAME = "careerpilot.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )
    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        education TEXT,
        skills TEXT,
        experience TEXT,
        resume TEXT,
        target_role TEXT,
        work_type TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
)

    conn.commit()
    conn.close()


def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def register_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    try:

        cursor.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash),
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def login_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        AND password_hash = ?
        """,
        (username, password_hash),
    )

    user = cursor.fetchone()

    conn.close()

    return user is not None

def get_user_id(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,),
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return user[0]

    return None


def save_profile(user_id, profile):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO profiles
        (
            user_id,
            name,
            education,
            skills,
            experience,
            resume,
            target_role,
            work_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            profile["name"],
            profile["education"],
            profile["skills"],
            profile["experience"],
            profile["resume"],
            profile["target_role"],
            profile["work_type"],
        ),
    )

    conn.commit()
    conn.close()

def get_profile(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            name,
            education,
            skills,
            experience,
            resume,
            target_role,
            work_type
        FROM profiles
        WHERE user_id = ?
        """,
        (user_id,),
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "name": row[0],
        "education": row[1],
        "skills": row[2],
        "experience": row[3],
        "resume": row[4],
        "target_role": row[5],
        "work_type": row[6],
    }