import json
from pathlib import Path
from datetime import datetime


class ServiceManager:
    def __init__(self, username, is_admin=False):
        self.username = username
        self.is_admin = is_admin

        base_dir = Path(__file__).resolve().parents[2]
        data_dir = base_dir / "System" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        self.file = data_dir / "services.json"

        self.services = {
            "network": {
                "description": "PyOS network service",
                "status": "RUNNING"
            },
            "database": {
                "description": "PyOS database service",
                "status": "RUNNING"
            },
            "logger": {
                "description": "PyOS logging service",
                "status": "RUNNING"
            },
            "scheduler": {
                "description": "PyOS task scheduler",
                "status": "STOPPED"
            }
        }

        self.load()

    def load(self):
        if not self.file.exists():
            self.save()
            return

        try:
            data = json.loads(self.file.read_text())

            if isinstance(data, dict):
                for name in self.services:
                    if name in data and isinstance(data[name], dict):
                        self.services[name]["status"] = data[name].get(
                            "status",
                            self.services[name]["status"]
                        )

        except (json.JSONDecodeError, OSError):
            pass

    def save(self):
        self.file.write_text(
            json.dumps(self.services, indent=4)
        )

    def list_services(self):
        print()
        print(f"{'SERVICE':<15}{'STATUS':<12}DESCRIPTION")
        print("-" * 65)

        for name, service in self.services.items():
            print(
                f"{name:<15}"
                f"{service['status']:<12}"
                f"{service['description']}"
            )

        print()
        return True

    def status(self, name):
        if name not in self.services:
            print(f"Service '{name}' not found.")
            return False

        service = self.services[name]

        print()
        print(f"Service:     {name}")
        print(f"Status:      {service['status']}")
        print(f"Description: {service['description']}")
        print()

        return True

    def start(self, name):
        if not self.is_admin:
            print("Permission denied. Administrator privileges required.")
            return False

        if name not in self.services:
            print(f"Service '{name}' not found.")
            return False

        if self.services[name]["status"] == "RUNNING":
            print(f"Service '{name}' is already running.")
            return False

        self.services[name]["status"] = "RUNNING"
        self.save()

        print(f"Service '{name}' started successfully.")
        return True

    def stop(self, name):
        if not self.is_admin:
            print("Permission denied. Administrator privileges required.")
            return False

        if name not in self.services:
            print(f"Service '{name}' not found.")
            return False

        if self.services[name]["status"] == "STOPPED":
            print(f"Service '{name}' is already stopped.")
            return False

        self.services[name]["status"] = "STOPPED"
        self.save()

        print(f"Service '{name}' stopped successfully.")
        return True

    def restart(self, name):
        if not self.is_admin:
            print("Permission denied. Administrator privileges required.")
            return False

        if name not in self.services:
            print(f"Service '{name}' not found.")
            return False

        self.services[name]["status"] = "RUNNING"
        self.save()

        print(f"Service '{name}' restarted successfully.")
        return True

    def execute(self, args):
        if not args:
            print(
                "Usage: service "
                "<list|status|start|stop|restart>"
            )
            return False

        command = args[0]

        if command == "list":
            return self.list_services()

        if command == "status":
            if len(args) != 2:
                print("Usage: service status <name>")
                return False
            return self.status(args[1])

        if command == "start":
            if len(args) != 2:
                print("Usage: service start <name>")
                return False
            return self.start(args[1])

        if command == "stop":
            if len(args) != 2:
                print("Usage: service stop <name>")
                return False
            return self.stop(args[1])

        if command == "restart":
            if len(args) != 2:
                print("Usage: service restart <name>")
                return False
            return self.restart(args[1])

        print(f"Unknown service command: {command}")
        return False