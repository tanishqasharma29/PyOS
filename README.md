<div align="center">

# PyOS

**A modular operating-system simulation built in Python**

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-educational-lightgrey)
![Tests](https://img.shields.io/badge/tests-10%20passing-brightgreen)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-informational)

</div>

PyOS is an educational, command-line operating-system simulation written in Python. It combines user authentication, a virtual filesystem with permissions, a feature-rich shell, process and job control, a scheduler, a service manager, simulated networking, a package manager, configuration, logging, and an automated test suite.

> **Note:** PyOS runs as a normal Python application. It is a learning tool, not a real kernel, and does not provide real operating-system security.

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Command Reference](#command-reference)
- [Project Structure](#project-structure)
- [Data Storage](#data-storage)
- [Testing](#testing)
- [Security](#security)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [License](#license)

---

## Features

| Area | Highlights |
|------|-----------|
| **Authentication** | Login system, administrator and standard accounts, bcrypt password hashing, user creation and management |
| **Virtual Filesystem** | Per-user home directories, `pwd` `ls` `cd` `touch` `cat` `write` `mkdir` `rm`, `stat` metadata, `chmod` permissions, user isolation |
| **Shell** | Command history, environment variables, pipes, redirection (`>`, `>>`), `&&` / `||`, command substitution `$()`, background jobs (`&`), `jobs` / `fg` / `bg`, `grep` |
| **Process Management** | `ps`, `start`, `kill`, process ownership, protected shell process, running/terminated states |
| **Networking** | `hostname`, `ping`, `ifconfig`, `netstat`, pipe-compatible output |
| **Package Manager** | `pkg list/installed/install/remove/info`, admin-only install/remove, persistent package database |
| **Scheduler** | Create, view, run and manage scheduled tasks |
| **Service Manager** | List, check status, start, stop and restart services |
| **Configuration** | View, get, set and reset configuration values |
| **Logging** | System activity log covering user, package, task and configuration events |
| **System Info** | OS/PyOS version, kernel, user, hostname, architecture, Python version, CPU cores, disk usage, time, uptime |
| **Boot System** | Simulated boot sequence initializing all subsystems |

**Simulated packages:** `calculator`, `editor`, `browser`, `terminal`

---

## Quick Start

### Prerequisites

- Python 3.9 or newer
- `pip`

### Installation

```bash
# Clone or open the project directory
cd PyOS

# Create and activate a virtual environment (macOS / Linux)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Dependency: `bcrypt==5.0.0`

### Run

```bash
python pyos.py
```

You will see the boot sequence, followed by the login manager:

```text
================================
          PyOS BOOT
================================

[ OK ] Preparing filesystem
[ OK ] Initializing database
[ OK ] Loading system configuration
[ OK ] Loading process manager
[ OK ] Loading service manager
[ OK ] Loading scheduler
[ OK ] Loading logger
[ OK ] Loading network subsystem

Boot completed successfully.

Starting login manager...
```

---

## Usage

### Login

```text
Username: root
Password:

Login successful!

Welcome to PyOS, root!
Account type: Administrator
```

### Example Session

```text
root@PyOS:/home/root$ touch test.txt
File created.

root@PyOS:/home/root$ write test.txt Hello
File written.

root@PyOS:/home/root$ cat test.txt
Hello

root@PyOS:/home/root$ stat test.txt

================================
        File Metadata
================================

Name:        test.txt
Type:        FILE
Size:        5 bytes
Owner:       root
Permissions: 644
Path:        /.../Filesystem/home/root/test.txt

root@PyOS:/home/root$ pkg list

PACKAGE        VERSION   DESCRIPTION
-------------------------------------------------------------
calculator     1.0       Simple calculator application
editor         1.0       Basic text editor application
browser        1.0       Basic web browser application
terminal       1.0       Terminal application
```

---

## Command Reference

### Filesystem

```text
pwd
ls
mkdir testdir
cd testdir
touch test.txt
write test.txt Hello
cat test.txt
stat test.txt
cd ..
```

### Permissions

```text
chmod 644 test.txt
chmod 400 test.txt
```

### Processes and Jobs

```text
ps
start editor
kill 2

start editor &
jobs
fg 2
bg 2
```

### Environment Variables

```text
set NAME Tanishqa
get NAME
echo $NAME
unset NAME
```

### Networking

```text
hostname
ping google.com 2
ifconfig
netstat
netstat | grep LISTEN
```

### Packages

```text
pkg list
pkg installed
pkg install calculator
pkg info calculator
pkg remove calculator
```

### Scheduler

```text
schedule list
schedule add backup 10
```

### Users

```text
user list
user info root
```

### System Information

```text
sysinfo
uname
uptime
date
time
```

### Configuration

```text
config list
config get hostname
config set hostname my-pyos
config reset
```

### Logs

```text
log show
log clear
```

### History

```text
history
history 5
clearhistory
```

---

## Project Structure

```text
PyOS/
├── pyos.py                  # Main entry point
├── requirements.txt
├── README.md
│
├── Filesystem/
│   └── home/
│       └── <users>
│
├── System/
│   ├── auth/
│   │   ├── login.py
│   │   └── passwords.py
│   │
│   ├── core/
│   │   ├── boot.py
│   │   ├── config_manager.py
│   │   ├── database.py
│   │   ├── environment.py
│   │   ├── filesystem.py
│   │   ├── history.py
│   │   ├── logger.py
│   │   ├── package_manager.py
│   │   ├── process.py
│   │   ├── scheduler.py
│   │   ├── service_manager.py
│   │   ├── shell.py         # Main shell implementation
│   │   ├── system.py
│   │   ├── system_info.py
│   │   └── user_manager.py
│   │
│   └── data/
│       ├── pyos.db
│       ├── packages.json
│       ├── history/
│       └── environment/
│
└── tests/
    └── test_pyos.py
```

Each subsystem lives in its own module so it can be developed and tested independently.

---

## Data Storage

Persistent data is stored in `System/data/`:

| File | Purpose |
|------|---------|
| `pyos.db` | SQLite database holding user information |
| `packages.json` | Package database |
| `history/<username>.json` | Per-user command history |
| `environment/<username>.json` | Per-user environment variables |

---

## Testing

```bash
# Compile check
python -m py_compile tests/test_pyos.py

# Run the full suite
python -m unittest discover tests -v
```

Expected result:

```text
Ran 10 tests

OK
```

**Coverage:** database initialization, user creation, environment variables, directory and file creation, file writing, package availability, process creation and termination, and shell-process protection.

---

## Security

PyOS simulates several security concepts for educational purposes:

- Bcrypt password hashing
- User roles and administrator privileges
- Filesystem ownership and permission modes
- Home-directory isolation
- Protected shell process
- Administrator-only package operations

These are not intended to provide real operating-system security.

---

## Limitations

PyOS is a simulation running as a normal Python application. It does not replace the host kernel and does not manage real hardware, CPU scheduling, memory protection, or physical devices. Networking, processes, packages, services, and scheduling are all simulated at the application level.

---

## Roadmap

- [ ] Virtual kernel architecture
- [ ] Improved process scheduling
- [ ] Memory management simulation
- [ ] Device management
- [ ] Additional shell utilities and better command parsing
- [ ] Expanded service management with boot-time dependencies
- [ ] User and group permissions
- [ ] Configuration files
- [ ] More realistic networking simulation
- [ ] Broader automated test coverage and documentation

---

## License

This project is intended for educational and academic use.
