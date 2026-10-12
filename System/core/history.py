import json
from pathlib import Path


class CommandHistory:

    def __init__(self, username):
        base_dir = Path(__file__).resolve().parents[2]
        history_dir = base_dir / "System" / "data" / "history"

        history_dir.mkdir(parents=True, exist_ok=True)

        self.file = history_dir / f"{username}.json"
        self.commands = []

        self.load()

    def load(self):
        if not self.file.exists():
            self.commands = []
            return

        try:
            self.commands = json.loads(
                self.file.read_text()
            )

            if not isinstance(self.commands, list):
                self.commands = []

        except (json.JSONDecodeError, OSError):
            self.commands = []

    def save(self):
        self.file.write_text(
            json.dumps(
                self.commands,
                indent=4
            )
        )

    def add(self, command):
        command = command.strip()

        if not command:
            return

        self.commands.append(command)
        self.save()

    def get(self, limit=None):
        if limit is None:
            return self.commands

        return self.commands[-limit:]

    def clear(self):
        self.commands = []
        self.save()