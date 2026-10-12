import bcrypt
from System.core.database import get_user


def authenticate(username, password):
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