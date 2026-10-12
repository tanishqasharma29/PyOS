import sqlite3
import bcrypt
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "System" / "data"
DB_PATH = DATA_DIR / "pyos.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def create_user(username, password, is_admin=False):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        hashed_password = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users (username, password, is_admin)
            VALUES (?, ?, ?)
            """,
            (
                username,
                hashed_password,
                int(is_admin)
            )
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_user(username):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, password, is_admin
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()
    connection.close()

    return user


def authenticate_user(username, password):
    user = get_user(username)

    if not user:
        return None

    stored_password = user[2]

    try:
        valid = bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        valid = password == stored_password

    if not valid:
        return None

    return {
        "id": user[0],
        "username": user[1],
        "is_admin": bool(user[3])
    }


def get_all_users():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, username, is_admin
            FROM users
            ORDER BY username
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()
def delete_user(username):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM users
            WHERE username = ?
            """,
            (username,)
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def change_password(username, password):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        hashed_password = hash_password(password)

        cursor.execute(
            """
            UPDATE users
            SET password = ?
            WHERE username = ?
            """,
            (hashed_password, username)
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()