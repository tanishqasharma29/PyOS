import json
import threading
from pathlib import Path
from datetime import datetime


class TaskManager:
    def __init__(self, username, is_admin=False, executor=None):
        self.username = username
        self.is_admin = is_admin
        self.executor = executor

        base_dir = Path(__file__).resolve().parents[2]
        data_dir = base_dir / "System" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        self.file = data_dir / "tasks.json"

        self.tasks = []
        self.next_id = 1
        self.timers = {}

        self.load()

    def set_executor(self, executor):
        self.executor = executor

    def load(self):
        if not self.file.exists():
            self.tasks = []
            self.next_id = 1
            self.save()
            return

        try:
            data = json.loads(self.file.read_text())

            if isinstance(data, list):
                self.tasks = data

                if self.tasks:
                    self.next_id = max(
                        task.get("id", 0)
                        for task in self.tasks
                    ) + 1
                else:
                    self.next_id = 1
            else:
                self.tasks = []
                self.next_id = 1

        except (json.JSONDecodeError, OSError):
            self.tasks = []
            self.next_id = 1

    def save(self):
        self.file.write_text(
            json.dumps(self.tasks, indent=4)
        )

    def add(self, name, command):
        if not name or not command:
            print("Task name and command are required.")
            return False

        task = {
            "id": self.next_id,
            "name": name,
            "command": command,
            "user": self.username,
            "status": "PENDING",
            "created": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "last_run": None,
            "scheduled_after": None
        }

        self.tasks.append(task)
        self.next_id += 1
        self.save()

        print(
            f"Task '{name}' added successfully "
            f"with ID {task['id']}."
        )

        return True

    def list_tasks(self):
        if not self.tasks:
            print("No scheduled tasks.")
            return True

        print()
        print(
            f"{'ID':<5}"
            f"{'NAME':<20}"
            f"{'STATUS':<12}"
            f"COMMAND"
        )
        print("-" * 70)

        for task in self.tasks:
            print(
                f"{task['id']:<5}"
                f"{task['name']:<20}"
                f"{task['status']:<12}"
                f"{task['command']}"
            )

        print()
        return True

    def get_task(self, task_id):
        try:
            task_id = int(task_id)
        except (ValueError, TypeError):
            return None

        for task in self.tasks:
            if task["id"] == task_id:
                return task

        return None

    def info(self, task_id):
        task = self.get_task(task_id)

        if task is None:
            print("Task not found.")
            return False

        print()
        print("Task Information")
        print("----------------")
        print(f"ID:              {task['id']}")
        print(f"Name:            {task['name']}")
        print(f"Command:         {task['command']}")
        print(f"User:            {task['user']}")
        print(f"Status:          {task['status']}")
        print(f"Created:         {task['created']}")
        print(
            f"Last Run:        "
            f"{task.get('last_run') or 'Never'}"
        )
        print(
            f"Scheduled After: "
            f"{task.get('scheduled_after') or 'Not scheduled'}"
        )
        print()

        return True

    def remove(self, task_id):
        task = self.get_task(task_id)

        if task is None:
            print("Task not found.")
            return False

        if not self.is_admin and task["user"] != self.username:
            print("Permission denied.")
            return False

        self.cancel(task_id, quiet=True)

        self.tasks.remove(task)
        self.save()

        print(
            f"Task '{task['name']}' removed successfully."
        )

        return True

    def run(self, task_id):
        task = self.get_task(task_id)

        if task is None:
            print("Task not found.")
            return False

        if not self.is_admin and task["user"] != self.username:
            print("Permission denied.")
            return False

        if self.executor is None:
            print("Task executor is not available.")
            return False

        task["status"] = "RUNNING"
        task["last_run"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.save()

        print()
        print(
            f"Running task '{task['name']}'..."
        )

        try:
            result = self.executor(task["command"])

            if result is False:
                task["status"] = "FAILED"
                self.save()
                print(
                    f"Task '{task['name']}' failed."
                )
                return False

            task["status"] = "COMPLETED"
            self.save()

            print(
                f"Task '{task['name']}' completed successfully."
            )

            return True

        except Exception as error:
            task["status"] = "FAILED"
            self.save()

            print(
                f"Task '{task['name']}' failed: {error}"
            )

            return False

    def schedule(self, task_id, seconds):
        task = self.get_task(task_id)

        if task is None:
            print("Task not found.")
            return False

        if not self.is_admin and task["user"] != self.username:
            print("Permission denied.")
            return False

        try:
            seconds = float(seconds)
        except (ValueError, TypeError):
            print("Invalid delay.")
            return False

        if seconds <= 0:
            print("Delay must be greater than zero.")
            return False

        self.cancel(task_id, quiet=True)

        task["status"] = "SCHEDULED"
        task["scheduled_after"] = seconds
        self.save()

        timer = threading.Timer(
            seconds,
            self._scheduled_run,
            args=(task["id"],)
        )

        timer.daemon = True
        self.timers[task["id"]] = timer
        timer.start()

        print(
            f"Task '{task['name']}' scheduled "
            f"to run in {seconds:g} seconds."
        )

        return True

    def _scheduled_run(self, task_id):
        self.timers.pop(task_id, None)

        task = self.get_task(task_id)

        if task is None:
            return

        task["scheduled_after"] = None
        self.save()

        self.run(task_id)

    def cancel(self, task_id, quiet=False):
        task = self.get_task(task_id)

        if task is None:
            if not quiet:
                print("Task not found.")
            return False

        if not self.is_admin and task["user"] != self.username:
            if not quiet:
                print("Permission denied.")
            return False

        timer = self.timers.pop(task["id"], None)

        if timer is not None:
            timer.cancel()

        if task["status"] == "SCHEDULED":
            task["status"] = "PENDING"
            task["scheduled_after"] = None
            self.save()

        if not quiet:
            print(
                f"Task '{task['name']}' cancelled."
            )

        return True

    def execute(self, args):
        if not args:
            print(
                "Usage: task "
                "<list|add|remove|run|schedule|cancel|info>"
            )
            return False

        command = args[0]

        if command == "list":
            return self.list_tasks()

        if command == "add":
            if len(args) < 3:
                print(
                    "Usage: task add <name> <command>"
                )
                return False

            name = args[1]
            task_command = " ".join(args[2:])

            return self.add(
                name,
                task_command
            )

        if command == "remove":
            if len(args) != 2:
                print(
                    "Usage: task remove <id>"
                )
                return False

            return self.remove(args[1])

        if command == "run":
            if len(args) != 2:
                print(
                    "Usage: task run <id>"
                )
                return False

            return self.run(args[1])

        if command == "schedule":
            if len(args) != 3:
                print(
                    "Usage: task schedule <id> <seconds>"
                )
                return False

            return self.schedule(
                args[1],
                args[2]
            )

        if command == "cancel":
            if len(args) != 2:
                print(
                    "Usage: task cancel <id>"
                )
                return False

            return self.cancel(args[1])

        if command == "info":
            if len(args) != 2:
                print(
                    "Usage: task info <id>"
                )
                return False

            return self.info(args[1])

        print(f"Unknown task command: {command}")
        return False