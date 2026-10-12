import json
from pathlib import Path


class PackageManager:

    def __init__(self, username, is_admin=False):
        self.username = username
        self.is_admin = is_admin

        base_dir = Path(__file__).resolve().parents[2]
        data_dir = base_dir / "System" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        self.file = data_dir / "packages.json"

        self.packages = {
            "calculator": {
                "version": "1.0",
                "description": "Simple calculator application"
            },
            "editor": {
                "version": "1.0",
                "description": "Basic text editor application"
            },
            "browser": {
                "version": "1.0",
                "description": "Basic web browser application"
            },
            "terminal": {
                "version": "1.0",
                "description": "Terminal application"
            }
        }

        self.installed = []
        self.load()

    def load(self):
        if not self.file.exists():
            self.installed = []
            self.save()
            return

        try:
            data = json.loads(self.file.read_text())
            if isinstance(data, list):
                self.installed = [
                    name for name in data
                    if name in self.packages
                ]
            else:
                self.installed = []
        except (json.JSONDecodeError, OSError):
            self.installed = []

    def save(self):
        self.file.write_text(
            json.dumps(self.installed, indent=4)
        )

    def list_available(self):
        print()
        print(
            f"{'PACKAGE':<15}"
            f"{'VERSION':<10}"
            f"DESCRIPTION"
        )
        print("-" * 65)

        for name, package in self.packages.items():
            print(
                f"{name:<15}"
                f"{package['version']:<10}"
                f"{package['description']}"
            )

        print()
        return True

    def list_installed(self):
        if not self.installed:
            print("No packages installed.")
            return True

        print()
        print(
            f"{'PACKAGE':<15}"
            f"{'VERSION':<10}"
            f"DESCRIPTION"
        )
        print("-" * 65)

        for name in self.installed:
            package = self.packages[name]
            print(
                f"{name:<15}"
                f"{package['version']:<10}"
                f"{package['description']}"
            )

        print()
        return True

    def install(self, name):
        if not self.is_admin:
            print(
                "Permission denied. "
                "Administrator privileges required."
            )
            return False

        if name not in self.packages:
            print(f"Package '{name}' not found.")
            return False

        if name in self.installed:
            print(f"Package '{name}' is already installed.")
            return False

        self.installed.append(name)
        self.save()

        print(
            f"Package '{name}' installed successfully."
        )
        return True

    def remove(self, name):
        if not self.is_admin:
            print(
                "Permission denied. "
                "Administrator privileges required."
            )
            return False

        if name not in self.installed:
            print(f"Package '{name}' is not installed.")
            return False

        self.installed.remove(name)
        self.save()

        print(
            f"Package '{name}' removed successfully."
        )
        return True

    def info(self, name):
        if name not in self.packages:
            print(f"Package '{name}' not found.")
            return False

        package = self.packages[name]
        status = (
            "installed"
            if name in self.installed
            else "not installed"
        )

        print()
        print(f"Name:        {name}")
        print(f"Version:     {package['version']}")
        print(f"Description: {package['description']}")
        print(f"Status:      {status}")
        print()

        return True

    def execute(self, args):
        if not args:
            print(
                "Usage: pkg "
                "<list|installed|install|remove|info>"
            )
            return False

        command = args[0]

        if command == "list":
            return self.list_available()

        if command == "installed":
            return self.list_installed()

        if command == "install":
            if len(args) != 2:
                print("Usage: pkg install <package>")
                return False
            return self.install(args[1])

        if command == "remove":
            if len(args) != 2:
                print("Usage: pkg remove <package>")
                return False
            return self.remove(args[1])

        if command == "info":
            if len(args) != 2:
                print("Usage: pkg info <package>")
                return False
            return self.info(args[1])

        print(f"Unknown package command: {command}")
        return False
