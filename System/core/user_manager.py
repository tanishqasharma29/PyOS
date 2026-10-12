from getpass import getpass
from System.core.database import get_all_users, create_user, get_user
from System.core.database import (
    create_user,
    get_all_users,
    get_user,
    delete_user,
    change_password
)


class UserManager:
    def __init__(self, username, is_admin=False):
        self.username = username
        self.is_admin = is_admin
    def info(self, args):
        if len(args) != 1:
            print("Usage: user info <username>")
            return False

        username = args[0]
        user = get_user(username)

        if not user:
            print(f"User '{username}' not found.")
            return False

        print()
        print("==============================")
        print("        User Information")
        print("==============================")
        print()
        print(f"ID:           {user[0]}")
        print(f"Username:     {user[1]}")
        print(f"Account Type: {'Administrator' if user[3] else 'Standard User'}")
        print()
        return True
    def list_users(self):
        users = get_all_users()

        if not users:
            print("No users found.")
            return True

        print()
        print(f"{'USERNAME':<20}{'TYPE'}")
        print("-" * 40)

        for user in users:
            username = user[1]
            user_type = (
                "Administrator"
                if user[2]
                else "Standard User"
            )

            print(f"{username:<20}{user_type}")

        print()
        return True

    def add_user(self, username):
        if not self.is_admin:
            print(
                "Permission denied. "
                "Administrator privileges required."
            )
            return False

        if not username:
            print("Username required.")
            return False

        if get_user(username):
            print(f"User '{username}' already exists.")
            return False

        password = getpass("Password: ")
        confirm = getpass("Confirm password: ")

        if password != confirm:
            print("Passwords do not match.")
            return False

        if not password:
            print("Password cannot be empty.")
            return False

        if create_user(username, password):
            print(
                f"User '{username}' "
                "created successfully."
            )
            return True

        print("Failed to create user.")
        return False

    def delete_user(self, username):
        if not self.is_admin:
            print(
                "Permission denied. "
                "Administrator privileges required."
            )
            return False

        if username == self.username:
            print("You cannot delete your own account.")
            return False

        user = get_user(username)

        if not user:
            print(f"User '{username}' not found.")
            return False

        if bool(user[3]):
            print("Administrator account cannot be deleted.")
            return False

        if delete_user(username):
            print(
                f"User '{username}' "
                "deleted successfully."
            )
            return True

        print("Failed to delete user.")
        return False

    def change_user_password(self, username=None):
        if username is None:
            username = self.username

        if username != self.username and not self.is_admin:
            print("Permission denied.")
            return False

        user = get_user(username)

        if not user:
            print(f"User '{username}' not found.")
            return False

        password = getpass("New password: ")
        confirm = getpass("Confirm new password: ")

        if password != confirm:
            print("Passwords do not match.")
            return False

        if not password:
            print("Password cannot be empty.")
            return False

        if change_password(username, password):
            print(
                f"Password for '{username}' "
                "changed successfully."
            )
            return True

        print("Failed to change password.")
        return False

    def execute(self, args):
        if not args:
            print(
                "Usage: user <list|add|delete|passwd>"
            )
            return False

        command = args[0]

        if command == "list":
            return self.list_users()

        if command == "add":
            if len(args) != 2:
                print("Usage: user add <username>")
                return False

            return self.add_user(args[1])

        if command == "delete":
            if len(args) != 2:
                print("Usage: user delete <username>")
                return False

            return self.delete_user(args[1])

        if command == "passwd":
            if len(args) == 1:
                return self.change_user_password()

            if len(args) == 2:
                return self.change_user_password(args[1])

            print("Usage: user passwd [username]")
            return False
        if command == "info":
            return self.info(args[1:])
        print(f"Unknown user command: {command}")
        return False