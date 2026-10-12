from getpass import getpass
from pathlib import Path

from System.core.boot import BootManager
from System.core.filesystem import FileSystem
from System.core.database import initialize_database, authenticate_user
from System.core.shell import Shell


def login():
    print()
    print("========================")
    print("         PyOS")
    print("========================")
    print()

    while True:
        username = input("Username: ").strip()
        password = getpass("Password: ")

        user = authenticate_user(
            username,
            password
        )

        if user:
            print()
            print("Login successful!")
            print()
            return user

        print()
        print("Invalid username or password.")
        print("Please try again.")
        print()


def main():

    boot = BootManager()

    if not boot.boot():
        return

    initialize_database()

    user = login()

    print(
        f"Welcome to PyOS, {user['username']}!"
    )

    if user["is_admin"]:
        print("Account type: Administrator")
    else:
        print("Account type: Standard User")

    print()

    filesystem_path = (
        Path(__file__).resolve().parent
        / "Filesystem"
    )

    filesystem = FileSystem(
        filesystem_path,
        user["username"],
        user["is_admin"]
    )

    shell = Shell(
        user,
        filesystem
    )

    while shell.running:

        try:
            command = input(
                shell.prompt()
            )

            shell.execute(command)

        except KeyboardInterrupt:
            print()
            print("Use 'exit' to leave PyOS.")

        except EOFError:
            print()
            break

    print("Goodbye!")


if __name__ == "__main__":
    main()