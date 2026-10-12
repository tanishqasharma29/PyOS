<div align="center">

  <img src="logo.png" alt="PyOS Logo" width="160" height="160">

  # PyOS

  **A Modular, Subsystem-Oriented Operating System Simulation Engine in Python**

  [![Python Version](https://img.shields.io/badge/python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![License](https://img.shields.io/badge/license-Educational-lightgrey?style=for-the-badge)](LICENSE)
  [![Tests](https://img.shields.io/badge/tests-10%20passing-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)](tests/)
  [![Architecture](https://img.shields.io/badge/architecture-Modular%20Monolith-orange?style=for-the-badge)]()
  [![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-informational?style=for-the-badge)]()

</div>

---

## Overview

**PyOS** is a modular, lightweight, command-line operating system simulation implemented purely in Python. Designed as an educational resource for computer science students and systems software enthusiasts, PyOS abstracts key kernel and user-space concepts including user authentication, virtual filesystem abstraction with permission modes, process control, background job management, service daemons, cron-like task scheduling, and package management.

> ⚠️ **Educational Disclaimer:** PyOS executes within standard Python user space. It serves as a pedagogical simulation tool rather than a standalone operating system kernel, and does not provide real operating-system security boundaries or hardware virtualization.

---

## Architecture Overview

PyOS is structured around a central shell processor that routes commands to independent, modular subsystems. Persistence is decoupled from in-memory process execution through SQLite and structured JSON state stores.

```text
+---------------------------------------------------------------------------------+
|                                PyOS Interactive Shell                           |
|                    (Command Parser, Piping, Redirection, Jobs)                  |
+---------------------------------------------------------------------------------+
                                         |
    +-------------------+----------------+--------------------+-------------------+
    |                   |                                     |                   |
    v                   v                                     v                   v
+-------+       +-------------------+                 +---------------+   +---------------+
| Auth  |       | Virtual FS Engine |                 | Process Ctrl  |   | System Config |
| Engine|       | Permissions (644) |                 | Job Control   |   | Environment   |
+-------+       +-------------------+                 +---------------+   +---------------+
    |                   |                                     |                   |
    +-------------------+----------------+--------------------+-------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                                Core Subsystems                                  |
|   [ Package Manager ]   [ Task Scheduler ]   [ Services ]   [ System Info ]     |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                                 Persistence Layer                               |
|        SQLite (pyos.db)   |   JSON Database Store   |   User Workspaces         |
+---------------------------------------------------------------------------------+
```

---

## Features

| Subsystem | Key Capabilities |
| :--- | :--- |
| **🔐 Authentication** | Role-based Access Control (Admin/User), `bcrypt` salt-and-hash password verification, user provisioning. |
| **📁 Virtual Filesystem** | Per-user sandboxed home directories, permission model (`chmod`), metadata inspection (`stat`), standard file I/O. |
| **💻 Interactive Shell** | Command history, environment variables (`$VAR`), standard piping (`\|`), redirection (`>`, `>>`), chained operators (`&&`, `\|\|`), job control (`&`, `jobs`, `fg`, `bg`). |
| **⚙️ Process Control** | PID allocation, background execution state tracking, process tree protection (protected parent shell PID), kill signals. |
| **📦 Package Manager** | Persistent package registry, dependency installation/removal semantics, privilege-restricted operation (`pkg`). |
| **⏱️ Scheduling & Services** | Delayed and recurring job execution, background daemon monitoring and state toggling (`start`, `stop`, `restart`). |
| **🌐 Network Simulation** | Virtual interface configuration (`ifconfig`), loopback ping tests, port listening table simulation (`netstat`). |
| **📊 Logging & Audit** | Structured event logging covering security events, system task state transitions, and package operations. |

---

## Quick Start

### Prerequisites

- **Python:** Version 3.9 or higher
- **Package Manager:** `pip`

### 1. Installation

Clone the repository and prepare the virtual environment:

```bash
# Clone the repository
git clone https://github.com/your-username/PyOS.git
cd PyOS

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### 2. Launching PyOS

Start the simulation by running the main entry script:

```bash
python pyos.py
```

Upon launch, PyOS runs its bootloader sequence to initialize all sub-modules:

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

## Command Reference Guide

### Filesystem & I/O

| Command | Description | Syntax / Example | Required Role |
| :--- | :--- | :--- | :--- |
| `pwd` | Print current working directory | `pwd` | Standard |
| `ls` | List directory contents | `ls` | Standard |
| `cd` | Change directory | `cd <path>` | Standard |
| `mkdir` | Create directory | `mkdir <dirname>` | Standard |
| `touch` | Create an empty file | `touch <filename>` | Standard |
| `cat` | Display file contents | `cat <filename>` | Standard |
| `write` | Overwrite file with text | `write <filename> <content>` | Standard |
| `stat` | Display file/directory metadata | `stat <filename>` | Standard |
| `chmod` | Modify permission bits | `chmod <octal> <filename>` | Standard |

### Process & Job Management

| Command | Description | Syntax / Example | Required Role |
| :--- | :--- | :--- | :--- |
| `ps` | Display running process table | `ps` | Standard |
| `start` | Launch process foreground or background | `start <app> [&]` | Standard |
| `kill` | Terminate process by PID | `kill <pid>` | Standard / Owner |
| `jobs` | List active background jobs | `jobs` | Standard |
| `fg` | Bring job to foreground | `fg <job_id>` | Standard |
| `bg` | Resume suspended job in background | `bg <job_id>` | Standard |

### System Administration & Packages

| Command | Description | Syntax / Example | Required Role |
| :--- | :--- | :--- | :--- |
| `pkg list` | List available packages | `pkg list` | Standard |
| `pkg install` | Install package from registry | `pkg install <pkg_name>` | Admin |
| `pkg remove` | Uninstall package | `pkg remove <pkg_name>` | Admin |
| `user list` | List all system accounts | `user list` | Admin |
| `config set` | Update system configuration | `config set <key> <val>` | Admin |
| `log show` | View system activity logs | `log show` | Admin |

---

## Project Structure

```text
PyOS/
├── pyos.py                  # Main kernel/shell entry point
├── requirements.txt         # External dependencies (bcrypt)
├── README.md                # System documentation
│
├── Filesystem/              # Virtual disk root
│   └── home/                # User workspace directories
│       ├── root/
│       └── <username>/
│
├── System/                  # System core core logic
│   ├── auth/                # Security subsystem
│   │   ├── login.py         # Login prompt & session handler
│   │   └── passwords.py     # Password hashing abstraction
│   │
│   ├── core/                # Core modular services
│   │   ├── boot.py          # System initialization sequence
│   │   ├── config_manager.py# Dynamic configuration loader
│   │   ├── database.py      # SQLite connection abstraction
│   │   ├── environment.py   # Shell environment variable table
│   │   ├── filesystem.py    # VFS abstraction layer
│   │   ├── history.py       # User command history management
│   │   ├── logger.py        # System event logger
│   │   ├── package_manager.py # Package management system
│   │   ├── process.py       # Process table & execution model
│   │   ├── scheduler.py     # Scheduled job daemon
│   │   ├── service_manager.py# System service daemon manager
│   │   ├── shell.py         # Shell parser & execution loop
│   │   ├── system.py        # System level utilities
│   │   ├── system_info.py   # Telemetry & info generator
│   │   └── user_manager.py  # User account management
│   │
│   └── data/                # Persistent system databases
│       ├── pyos.db          # User database (SQLite)
│       ├── packages.json    # Package repository catalog
│       ├── history/         # Per-user command history stores
│       └── environment/     # Per-user environment persistence
│
└── tests/                   # Automated unit test suite
    └── test_pyos.py
```

---

## Data Persistence & Schemas

System state is stored under `System/data/`:

### SQLite Database (`pyos.db`)
Stores account credentials and user privilege levels.

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Structured Files
- **`packages.json`**: Package registry and installation state index.
- **`history/<username>.json`**: Command line history array per user context.
- **`environment/<username>.json`**: Key-value mapping for persistent environment variable mappings.

---

## Testing & Quality Assurance

PyOS includes an automated `unittest` suite covering user creation, filesystem operations, process security, and command parsing.

### Executing Tests

```bash
# Verify test file syntax
python -m py_compile tests/test_pyos.py

# Run the full test suite with verbose output
python -m unittest discover -s tests -p "test_*.py" -v
```

### Test Coverage Highlights
- ✅ **Database Initialization:** Validates table creation and schema integrity.
- ✅ **Authentication:** Verifies `bcrypt` hashing and user credential verification.
- ✅ **Virtual Filesystem:** Tests path isolation, permission checking, and file operations.
- ✅ **Process Protection:** Verifies that critical processes (such as the main shell PID) cannot be killed.

---

## Security Architecture

| Security Feature | Implementation Mechanism |
| :--- | :--- |
| **Credential Protection** | Passwords are salted and hashed using `bcrypt` (5.0+). Plaintext passwords are never stored. |
| **Privilege Separation** | Administrative tasks (`pkg install`, `config set`, user management) require elevated root status. |
| **Isolation** | User environments and standard directory paths are restricted based on permissions. |
| **Process Control** | Key process IDs (PID 1 / Shell) are protected against termination by standard user sessions. |

---

## Limitations

- **Process Emulation:** Processes run as simulated objects in standard Python memory space; they are not native host operating system processes.
- **Hardware Abstraction:** No real hardware interaction (CPU scheduling, physical memory management, or hardware device drivers) takes place.
- **Security Scope:** PyOS does not provide security containment against host system level threats; it is strictly an educational application simulation.

---

## Roadmap

- [ ] **Virtual Kernel Architecture:** Introduce kernel mode vs. user mode execution abstractions.
- [ ] **Memory Allocation Simulator:** Emulate virtual memory, paging, and page replacement algorithms (LRU, FIFO).
- [ ] **Preemptive Scheduler:** Implement Round-Robin and Priority-based CPU scheduling models.
- [ ] **Extended Networking Layer:** Add simulated TCP socket handling and virtual HTTP server daemon.
- [ ] **Multi-User Concurrent Sessions:** Allow multiple virtual shell sessions over terminal connections.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/NewFeature`).
3. Commit your updates (`git commit -m 'Add NewFeature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request with a clear description of changes.

---

## License

Distributed under the MIT License for educational and academic purposes. See `LICENSE` for details.
