import json
from pathlib import Path
from datetime import datetime


class Logger:
    def __init__(self, username):
        self.username = username

        base_dir = Path(__file__).resolve().parents[2]
        data_dir = base_dir / "System" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        self.file = data_dir / "system.log"

    def write(self, action, details=""):
        entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": self.username,
            "action": action,
            "details": details
        }

        with self.file.open("a") as file:
            file.write(json.dumps(entry) + "\n")

    def show(self, limit=None):
        if not self.file.exists():
            print("No log entries found.")
            return True

        try:
            lines = self.file.read_text().splitlines()
        except OSError:
            print("Unable to read log file.")
            return False

        if limit is not None:
            try:
                limit = int(limit)
            except ValueError:
                print("Invalid log limit.")
                return False

            if limit <= 0:
                print("Limit must be greater than 0.")
                return False

            lines = lines[-limit:]

        if not lines:
            print("No log entries found.")
            return True

        print()
        print(f"{'TIME':<21}{'USER':<15}{'ACTION':<20}DETAILS")
        print("-" * 85)

        for line in lines:
            try:
                entry = json.loads(line)

                print(
                    f"{entry['time']:<21}"
                    f"{entry['user']:<15}"
                    f"{entry['action']:<20}"
                    f"{entry['details']}"
                )

            except (json.JSONDecodeError, KeyError):
                continue

        print()
        return True

    def clear(self):
        self.file.write_text("")
        print("System log cleared.")
        return True

    def execute(self, args):
        if not args:
            return self.show()

        command = args[0]

        if command == "show":
            if len(args) == 1:
                return self.show()

            if len(args) == 2:
                return self.show(args[1])

            print("Usage: log show [limit]")
            return False

        if command == "clear":
            return self.clear()

        print(f"Unknown log command: {command}")
        return False