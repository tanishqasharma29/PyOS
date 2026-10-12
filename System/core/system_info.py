import platform
import os
import shutil
import time
from datetime import datetime


class SystemInfo:

    def __init__(self, username, hostname="pyos"):
        self.username = username
        self.hostname = hostname
        self.start_time = time.time()

    def get_uptime(self):
        seconds = int(time.time() - self.start_time)

        days = seconds // 86400
        seconds %= 86400

        hours = seconds // 3600
        seconds %= 3600

        minutes = seconds // 60
        seconds %= 60

        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"

        if minutes > 0:
            return f"{minutes}m {seconds}s"

        return f"{seconds}s"

    def get_disk_info(self):
        total, used, free = shutil.disk_usage("/")

        total_gb = total / (1024 ** 3)
        used_gb = used / (1024 ** 3)
        free_gb = free / (1024 ** 3)

        return total_gb, used_gb, free_gb

    def show(self):

        total, used, free = self.get_disk_info()

        print()
        print("==============================")
        print("       PyOS System Info")
        print("==============================")
        print()

        print(f"OS:           PyOS")
        print(f"Version:      1.0")
        print(f"Kernel:       PyOS Kernel 1.0")
        print(f"User:         {self.username}")
        print(f"Hostname:     {self.hostname}")
        print(f"Architecture: {platform.machine()}")
        print(f"Platform:     {platform.system()}")
        print(f"Python:       {platform.python_version()}")
        print(f"CPU Cores:    {os.cpu_count()}")
        print(f"Disk Total:   {total:.2f} GB")
        print(f"Disk Used:    {used:.2f} GB")
        print(f"Disk Free:    {free:.2f} GB")
        print(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Uptime:       {self.get_uptime()}")

        print()

        return True

    def uname(self):

        print()
        print("PyOS")
        print("Kernel: PyOS Kernel 1.0")
        print(f"Architecture: {platform.machine()}")
        print(f"Python: {platform.python_version()}")
        print()

        return True

    def hostname_command(self):

        print(self.hostname)
        return True

    def uptime_command(self):

        print(f"Uptime: {self.get_uptime()}")
        return True