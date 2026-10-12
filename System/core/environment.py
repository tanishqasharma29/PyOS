import json
import re
from pathlib import Path


class EnvironmentManager:

    def __init__(self, username):
        base_dir = Path(__file__).resolve().parents[2]

        environment_dir = (
            base_dir
            / "System"
            / "data"
            / "environment"
        )

        environment_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.file = environment_dir / f"{username}.json"
        self.variables = {}

        self.load()

    def load(self):
        if not self.file.exists():
            self.variables = {}
            return

        try:
            data = json.loads(
                self.file.read_text()
            )

            if isinstance(data, dict):
                self.variables = data
            else:
                self.variables = {}

        except (json.JSONDecodeError, OSError):
            self.variables = {}

    def save(self):
        self.file.write_text(
            json.dumps(
                self.variables,
                indent=4
            )
        )

    def valid_name(self, name):
        return bool(
            re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_]*",
                name
            )
        )

    def set(self, name, value):
        if not self.valid_name(name):
            return False, "Invalid variable name."

        self.variables[name] = value
        self.save()

        return True, "Variable set."

    def get(self, name):
        if name not in self.variables:
            return False, "Variable not found."

        return True, self.variables[name]

    def unset(self, name):
        if name not in self.variables:
            return False, "Variable not found."

        del self.variables[name]
        self.save()

        return True, "Variable removed."

    def get_all(self):
        return dict(
            sorted(self.variables.items())
        )

    def clear(self):
        self.variables = {}
        self.save()