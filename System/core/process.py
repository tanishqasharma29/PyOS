from datetime import datetime


class ProcessManager:

    def __init__(self):
        self.next_pid = 1

        self.processes = [
            {
                "pid": self.next_pid,
                "user": "root",
                "name": "shell",
                "status": "RUNNING",
                "started": datetime.now()
            }
        ]

        self.next_pid += 1

    def create_process(self, user, name):
        if not name:
            return False, "Process name required."

        process = {
            "pid": self.next_pid,
            "user": user,
            "name": name,
            "status": "RUNNING",
            "started": datetime.now()
        }

        self.processes.append(process)
        self.next_pid += 1

        return True, process["pid"]

    def kill_process(self, pid, user, is_admin=False):
        try:
            pid = int(pid)
        except ValueError:
            return False, "Invalid PID."

        for process in self.processes:

            if process["pid"] != pid:
                continue

            if process["name"] == "shell":
                return False, "Cannot terminate shell process."

            if process["status"] == "TERMINATED":
                return False, "Process already terminated."

            if not is_admin and process["user"] != user:
                return False, "Permission denied."

            process["status"] = "TERMINATED"

            return True, "Process terminated."

        return False, "Process not found."

    def get_processes(self):
        return self.processes

    def get_process(self, pid):
        try:
            pid = int(pid)
        except ValueError:
            return None

        for process in self.processes:
            if process["pid"] == pid:
                return process

        return None

    def get_running_processes(self):
        return [
            process
            for process in self.processes
            if process["status"] == "RUNNING"
        ]