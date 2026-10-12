import json
from pathlib import Path
from datetime import datetime, timedelta


class Scheduler:
    def __init__(self, username, is_admin=False):
        self.username = username
        self.is_admin = is_admin

        base_dir = Path(__file__).resolve().parents[2]
        data_dir = base_dir / "System" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        self.file = data_dir / "scheduler.json"

        self.tasks = []
        self.next_id = 1

        self.load()

    def load(self):
        if not self.file.exists():
            self.save()
            return

        try:
            data = json.loads(self.file.read_text())

            if isinstance(data, list):
                self.tasks = data

                if self.tasks:
                    self.next_id = max(
                        task["id"] for task in self.tasks
                    ) + 1

        except (json.JSONDecodeError, OSError, ValueError):
            self.tasks = []
            self.next_id = 1

    def save(self):
        self.file.write_text(
            json.dumps(self.tasks, indent=4)
        )

    def update_status(self):
        now = datetime.now()

        changed = False

        for task in self.tasks:
            if task["status"] == "SCHEDULED":
                run_at = datetime.fromisoformat(task["run_at"])

                if now >= run_at:
                    task["status"] = "READY"
                    changed = True

        if changed:
            self.save()

    def list_tasks(self):
        self.update_status()

        if not self.tasks:
            print("No scheduled tasks.")
            return True

        print()
        print(
            f"{'ID':<6}"
            f"{'NAME':<15}"
            f"{'STATUS':<12}"
            f"{'RUN AT':<22}"
        )
        print("-" * 60)

        for task in self.tasks:
            print(
                f"{task['id']:<6}"
                f"{task['name']:<15}"
                f"{task['status']:<12}"
                f"{task['run_at']}"
            )

        print()
        return True

    def add(self, name, seconds):
        if not self.is_admin:
            print(
                "Permission denied. "
                "Administrator privileges required."
            )
            return False

        if not name:
            print("Task name required.")
            return False

        try:
            seconds = int(seconds)
        except ValueError:
            print("Delay must be a number.")
            return False

        if seconds <= 0:
            print("Delay must be greater than 0.")
            return False

        run_at = datetime.now() + timedelta(seconds=seconds)

        task = {
            "id": self.next_id,
            "name": name,
            "status": "SCHEDULED",
            "delay": seconds,
            "run_at": run_at.isoformat(
                timespec="seconds"
            ),
            "created_by": self.username
        }

        self.tasks.append(task)
        self.next_id += 1

        self.save()

        print()
        print("Task scheduled successfully.")
        print(f"Task ID: {task['id']}")
        print(f"Name:    {name}")
        print(f"Runs at: {task['run_at']}")
        print()

        return True

    def remove(self, task_id):
        if not self.is_admin:
            print(
                "Permission denied. "
                "Administrator privileges required."
            )
            return False

        try:
            task_id = int(task_id)
        except ValueError:
            print("Invalid task ID.")
            return False

        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.save()

                print(
                    f"Task {task_id} removed successfully."
                )

                return True

        print(f"Task {task_id} not found.")
        return False

    def run(self, task_id):
        if not self.is_admin:
            print(
                "Permission denied. "
                "Administrator privileges required."
            )
            return False

        self.update_status()

        try:
            task_id = int(task_id)
        except ValueError:
            print("Invalid task ID.")
            return False

        for task in self.tasks:
            if task["id"] == task_id:

                if task["status"] == "SCHEDULED":
                    print(
                        "Task is not ready yet."
                    )
                    return False

                if task["status"] == "COMPLETED":
                    print(
                        "Task has already been completed."
                    )
                    return False

                task["status"] = "COMPLETED"
                self.save()

                print()
                print(
                    f"Task {task_id} "
                    f"'{task['name']}' executed successfully."
                )
                print()

                return True

        print(f"Task {task_id} not found.")
        return False

    def execute(self, args):
        if not args:
            print(
                "Usage: schedule "
                "<list|add|remove|run>"
            )
            return False

        command = args[0]

        if command == "list":
            return self.list_tasks()

        if command == "add":
            if len(args) != 3:
                print(
                    "Usage: schedule add "
                    "<name> <seconds>"
                )
                return False

            return self.add(
                args[1],
                args[2]
            )

        if command == "remove":
            if len(args) != 2:
                print(
                    "Usage: schedule remove <id>"
                )
                return False

            return self.remove(args[1])

        if command == "run":
            if len(args) != 2:
                print(
                    "Usage: schedule run <id>"
                )
                return False

            return self.run(args[1])

        print(f"Unknown scheduler command: {command}")
        return False