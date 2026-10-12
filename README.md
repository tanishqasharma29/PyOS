

# PyOS

PyOS is a toy operating system simulation built in Python. It provides a command-line environment with user authentication, a virtual filesystem, permissions, process management, scheduling, services, networking, package management, configuration, logging, and automated tests.

## Features

### Authentication
- User login system
- Administrator and standard-user accounts
- Bcrypt password hashing
- User creation and management

### Virtual Filesystem
- Home directories for users
- `pwd`, `ls`, `cd`
- File creation and deletion
- `touch`, `cat`, `write`
- Directory creation and removal
- File metadata with `stat`
- Permission management with `chmod`
- User-based filesystem isolation

### Shell
- Interactive PyOS shell
- Command history
- Environment variables
- Pipes
- Output redirection with `>` and `>>`
- `&&` and `||`
- Command substitution with `$()`
- Background processes with `&`
- Job control with `jobs`, `fg`, and `bg`
- `grep`

### Process Management
- `ps`
- `start`
- `kill`
- Process ownership
- Shell protection
- Running/terminated process states

### Networking
- `hostname`
- `ping`
- `ifconfig`
- `netstat`
- Network command piping

### Package Manager
- `pkg list`
- `pkg installed`
- `pkg install <package>`
- `pkg remove <package>`
- `pkg info <package>`
- Administrator-only package installation/removal
- Persistent package database

Available simulated packages include:
- calculator
- editor
- browser
- terminal

### Scheduler
- Create scheduled tasks
- View scheduled tasks
- Run and manage scheduled jobs

### Service Manager
- List services
- Check service status
- Start and stop services
- Restart services

### Configuration
- View configuration
- Get individual configuration values
- Change configuration values
- Reset configuration

Example:
```text
config list
config get hostname
config set hostname my-pyos
config reset
```

### Logging
- System activity logging
- View logs
- Clear logs
- Logs include actions such as user creation, package installation, task creation, and configuration changes

Example:
```text
log show
log clear
```

### System Information
PyOS provides system information such as:
- OS and PyOS version
- Kernel
- Current user
- Hostname
- Architecture
- Python version
- CPU cores
- Disk usage
- Current time
- Uptime

### Boot System
PyOS includes a simulated boot sequence that initializes:
- Filesystem
- Database
- Configuration
- Process manager
- Service manager
- Scheduler
- Logger
- Network subsystem

## Project Structure

```text
PyOS/
│
├── pyos.py
├── requirements.txt
├── README.md
│
├── Filesystem/
│   └── home/
│       └── <users>
│
├── System/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── login.py
│   │   └── passwords.py
│   │
│   ├── core/
│   │   ├── __init__.py
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
│   │   ├── shell.py
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
├── tests/
│   └── test_pyos.py
│
└── .venv/
```

## Requirements

- Python 3.9+
- `bcrypt`

The project uses:

```text
bcrypt==5.0.0
```

## Installation

Clone or open the project directory:

```bash
cd PyOS
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running PyOS

Start the operating system with:

```bash
python pyos.py
```

You should see the PyOS boot sequence followed by the login manager.

Example:

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

## Login

After boot, enter your username and password.

Example:

```text
Username: root
Password:
```

After successful authentication:

```text
Login successful!

Welcome to PyOS, root!
Account type: Administrator
```

## Example Commands

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

### Processes

```text
ps
start editor
kill 2
```

### Jobs

```text
start editor &
jobs
fg 2
bg 2
```

### Environment

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

## Testing

PyOS includes a unit-test suite.

Compile the tests:

```bash
python -m py_compile tests/test_pyos.py
```

Run all tests:

```bash
python -m unittest discover tests -v
```

Expected result:

```text
Ran 10 tests

OK
```

The tests currently cover:
- Database initialization
- User creation
- Environment variables
- Filesystem directory creation
- Filesystem file creation
- File writing
- Package availability
- Process creation
- Process termination
- Protection of the shell process

## Security

PyOS includes several simulated security features:

- Bcrypt password hashing
- User roles
- Administrator privileges
- Filesystem ownership
- Permission modes
- User home-directory isolation
- Protected shell process
- Administrator-only package operations

This is an educational operating-system simulation and is not intended to provide real operating-system security.

## Data Storage

Persistent PyOS data is stored inside:

```text
System/data/
```

Important files include:

```text
pyos.db
packages.json
history/<username>.json
environment/<username>.json
```

The SQLite database stores user information, while JSON files store package, command-history, and environment-variable data.

## Example Session

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

## Development

PyOS is designed as a modular educational project. Core operating-system functionality is separated into modules so that individual subsystems can be developed and tested independently.

Main entry point:

```text
pyos.py
```

Main shell implementation:

```text
System/core/shell.py
```

## Limitations

PyOS is a simulation running as a normal Python application. It does not replace the host operating system kernel and does not directly manage real hardware, CPU scheduling, memory protection, or physical devices.

Several components, including networking, processes, packages, services, and scheduling, are simulated at the application level.

## Future Improvements

Possible future extensions include:

- More complete virtual kernel architecture
- Improved process scheduling
- Memory management simulation
- Device management
- More shell utilities
- Better command parsing
- Expanded service management
- More extensive automated testing
- Improved documentation
- User and group permissions
- Configuration files
- Boot-time service dependencies
- More realistic networking simulation

## License

This project is intended for educational and academic use.
