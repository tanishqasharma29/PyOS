import json
from pathlib import Path


class ConfigManager:
    def __init__(self, username, is_admin=False):
        self.username = username
        self.is_admin = is_admin

        base_dir = Path(__file__).resolve().parents[2]
        data_dir = base_dir / "System" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        self.file = data_dir / "config.json"

        self.defaults = {
            "hostname": "pyos",
            "version": "1.0",
            "kernel": "PyOS Kernel 1.0",
            "default_shell": "PyOS Shell",
            "language": "Python",
            "timezone": "IST"
        }

        self.config = {}
        self.load()

    def load(self):
        if not self.file.exists():
            self.config = dict(self.defaults)
            self.save()
            return

        try:
            data = json.loads(self.file.read_text())

            if isinstance(data, dict):
                self.config = dict(self.defaults)
                self.config.update(data)
            else:
                self.config = dict(self.defaults)

        except (json.JSONDecodeError, OSError):
            self.config = dict(self.defaults)

    def save(self):
        self.file.write_text(
            json.dumps(self.config, indent=4)
        )

    def list_config(self):
        print()
        print(f"{'KEY':<20}VALUE")
        print("-" * 50)

        for key, value in self.config.items():
            print(f"{key:<20}{value}")

        print()
        return True

    def get(self, key):
        if key not in self.config:
            print(f"Configuration key '{key}' not found.")
            return False

        print(f"{key}: {self.config[key]}")
        return True

    def set(self, key, value):
        if not self.is_admin:
            print(
                "Permission denied. "
                "Administrator privileges required."
            )
            return False

        if not key:
            print("Configuration key required.")
            return False

        if key not in self.defaults:
            print(f"Unknown configuration key: {key}")
            return False

        if not value:
            print("Configuration value required.")
            return False

        self.config[key] = value
        self.save()

        print(
            f"Configuration '{key}' "
            "updated successfully."
        )

        return True

    def reset(self):
        if not self.is_admin:
            print(
                "Permission denied. "
                "Administrator privileges required."
            )
            return False

        self.config = dict(self.defaults)
        self.save()

        print("Configuration reset successfully.")
        return True

    def execute(self, args):
        if not args:
            return self.list_config()

        command = args[0]

        if command == "list":
            return self.list_config()

        if command == "get":
            if len(args) != 2:
                print("Usage: config get <key>")
                return False

            return self.get(args[1])

        if command == "set":
            if len(args) < 3:
                print("Usage: config set <key> <value>")
                return False

            key = args[1]
            value = " ".join(args[2:])

            return self.set(key, value)

        if command == "reset":
            return self.reset()

        print(f"Unknown config command: {command}")
        return False