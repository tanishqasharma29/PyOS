import os
import platform
import socket
import subprocess
from datetime import datetime


PYOS_VERSION = "1.0.0"


def sysinfo():
    print()
    print("PyOS System Information")
    print("------------------------")
    print(f"PyOS Version : {PYOS_VERSION}")
    print(f"Platform     : {platform.system()}")
    print(f"Architecture : {platform.machine()}")
    print(f"Python       : {platform.python_version()}")
    print(f"Hostname     : {socket.gethostname()}")
    print(f"CPU Count    : {os.cpu_count()}")
    print()


def show_date():
    print(datetime.now().strftime("%Y-%m-%d"))


def show_time():
    print(datetime.now().strftime("%H:%M:%S"))


def hostname():
    print(socket.gethostname())


def uname():
    information = platform.uname()

    print()
    print("System      :", information.system)
    print("Node        :", information.node)
    print("Release     :", information.release)
    print("Version     :", information.version)
    print("Machine     :", information.machine)
    print("Processor   :", information.processor)
    print()


def uptime():
    try:
        result = subprocess.run(
            ["uptime"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print("Unable to determine uptime.")

    except Exception:
        print("Unable to determine uptime.")


def processes():
    try:
        result = subprocess.run(
            ["ps", "-o", "pid,ppid,stat,comm"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(result.stdout.rstrip())
        else:
            print("Unable to retrieve processes.")

    except Exception:
        print("Unable to retrieve processes.")