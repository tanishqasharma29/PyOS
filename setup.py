from System.core.database import initialize_database, create_user
from System.auth.passwords import hash_password


initialize_database()

username = input("Enter username: ")
password = input("Enter password: ")

hashed_password = hash_password(password)

if create_user(username, hashed_password, True):
    print("User created successfully.")
else:
    print("Username already exists.")