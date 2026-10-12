import os



import shlex



import socket



import platform

from System.core.task_manager import TaskManager

import subprocess



from datetime import datetime



from getpass import getpass







from System.core.database import create_user, get_all_users



from System.core.process import ProcessManager



from System.core.history import CommandHistory



from System.core.environment import EnvironmentManager

from System.core.package_manager import PackageManager

from System.core.service_manager import ServiceManager

from System.core.scheduler import Scheduler

from System.core.user_manager import UserManager

from System.core.logger import Logger

from System.core.system_info import SystemInfo



from System.core.config_manager import ConfigManager







class Shell:

    def __init__(self, user, filesystem):



        self.user = user



        self.filesystem = filesystem







        self.running = True







        self.process_manager = ProcessManager()



        self.history = CommandHistory(



            self.user["username"]



        )



        self.environment = EnvironmentManager(



            self.user["username"]



        )



        self.package_manager = PackageManager(



            self.user["username"],



            self.user["is_admin"]



        )

        self.task_manager = TaskManager(
            self.user["username"],
            self.user["is_admin"],
            self.execute
        )

        self.service_manager = ServiceManager(

            self.user["username"],

            self.user["is_admin"]

        )



        self.scheduler = Scheduler(

            self.user["username"],

            self.user["is_admin"]

        )



        self.user_manager = UserManager(

            self.user["username"],

            self.user["is_admin"]

        )



        self.logger = Logger(

            self.user["username"]

        )

        self.config_manager = ConfigManager(

            self.user["username"],

            self.user["is_admin"]

        )

        self.system_info = SystemInfo(

            self.user["username"]

        )







    def prompt(self):



        return (



            f"{self.user['username']}@PyOS:"



            f"{self.filesystem.display_path()}$ "



        )







    def log_action(self, command, success):



        if not success:

            return



        try:

            parts = shlex.split(command)

        except ValueError:

            return



        if not parts:

            return



        cmd = parts[0]

        args = parts[1:]



        if cmd == "log":

            return



        action = None

        details = " ".join(args)



        action_map = {

            "start": "PROCESS_START",

            "kill": "PROCESS_KILL",

            "mkdir": "DIRECTORY_CREATE",

            "rmdir": "DIRECTORY_REMOVE",

            "touch": "FILE_CREATE",

            "write": "FILE_WRITE",

            "rm": "FILE_REMOVE",

            "chmod": "PERMISSION_CHANGE"

        }



        if cmd in action_map:

            action = action_map[cmd]



        elif cmd == "user" and args:

            action = {

                "add": "USER_CREATE",

                "delete": "USER_DELETE",

                "passwd": "PASSWORD_CHANGE"

            }.get(args[0])

            details = " ".join(args[1:])

        elif cmd == "pkg" and args:

            action = {

                "install": "PACKAGE_INSTALL",

                "remove": "PACKAGE_REMOVE"

            }.get(args[0])

            details = " ".join(args[1:])



        elif cmd == "service" and args:

            action = {

                "start": "SERVICE_START",

                "stop": "SERVICE_STOP",

                "restart": "SERVICE_RESTART"

            }.get(args[0])

            details = " ".join(args[1:])



        elif cmd == "schedule" and args:

            action = {

                "add": "TASK_CREATE",

                "remove": "TASK_REMOVE",

                "run": "TASK_RUN"

            }.get(args[0])

            details = " ".join(args[1:])

        elif cmd == "config" and args:

            action = {

                "set": "CONFIG_SET",

                "reset": "CONFIG_RESET"

            }.get(args[0])

            details = " ".join(args[1:])

        elif cmd == "user" and args:

            action = {

                "add": "USER_CREATE",

                "delete": "USER_DELETE",

                "passwd": "PASSWORD_CHANGE"

            }.get(args[0])

            details = " ".join(args[1:])



        elif cmd == "adduser" and args:

            action = "USER_CREATE"

            details = args[0]



        if action:

            try:

                self.logger.write(action, details)

            except Exception:

                pass





    def execute(self, command, record_history=True):







        command = command.strip()







        if not command:



            return True



        background = False







        if command.endswith("&"):



            background = True



            command = command[:-1].strip()







        if not command:



            print("Background command required.")



            return False



        if record_history:



            self.history.add(command)







        command = self.expand_variables(command)



        command = self.expand_command_substitution(command)







        if "||" in command:



            parts = command.split("||", 1)







            first = parts[0].strip()



            second = parts[1].strip()







            success = self.execute(



                first,



                record_history=False



            )







            if not success:



                return self.execute(



                    second,



                    record_history=False



                )







            return True







        if "&&" in command:



            parts = command.split("&&", 1)







            first = parts[0].strip()



            second = parts[1].strip()







            success = self.execute(



                first,



                record_history=False



            )







            if success:



                return self.execute(



                    second,



                    record_history=False



                )







            return False







        if "|" in command:



            return self.execute_pipe(command)







        redirected = self.handle_redirection(command)







        if redirected is not None:



            command, redirect_type, filename = redirected



            return self.execute_redirected(



                command,



                redirect_type,



                filename



            )







        try:



            args = shlex.split(command)



        except ValueError as error:



            print(f"Syntax error: {error}")



            return False







        if not args:



            return True







        name = args[0]



        args = args[1:]







        commands = {



            "help": lambda: self.help(),



            "clear": lambda: self.clear(),



            "echo": lambda: self.echo(args),



            "pwd": lambda: self.pwd(),



            "whoami": lambda: self.whoami(),



            "exit": lambda: self.exit(),

            "stat": lambda: self.stat(args),





            "sysinfo": lambda: self.sysinfo(),



            "date": lambda: self.date(),



            "time": lambda: self.time(),



            "hostname": lambda: self.hostname(),



            "uname": lambda: self.uname(),



            "uptime": lambda: self.uptime(),



            "ping": lambda: self.ping(args),



            "ifconfig": lambda: self.ifconfig(),



            "netstat": lambda: self.netstat(),



            "ps": lambda: self.ps(),



            "jobs": lambda: self.jobs(),



            "fg": lambda: self.fg(args),



            "bg": lambda: self.bg(args),



            "start": lambda: self.start(args),



            "kill": lambda: self.kill(args),



            "process": lambda: self.process(args),







            "users": lambda: self.users(),



            "adduser": lambda: self.adduser(args),







            "ls": lambda: self.ls(args),



            "mkdir": lambda: self.mkdir(args),



            "cd": lambda: self.cd(args),



            "rmdir": lambda: self.rmdir(args),



            "touch": lambda: self.touch(args),



            "write": lambda: self.write(args),



            "rm": lambda: self.rm(args),



            "cat": lambda: self.cat(args),



            "chmod": lambda: self.chmod(args),



            "permissions": lambda: self.permissions(args),

            "stat": lambda: self.stat(args),





            "history": lambda: self.show_history(args),



            "clearhistory": lambda: self.clear_history(),







            "env": lambda: self.env(),



            "set": lambda: self.set_variable(args),



            "get": lambda: self.get_variable(args),



            "unset": lambda: self.unset_variable(args),



            "pkg": lambda: self.package_manager.execute(args),
            "task": lambda: self.task_manager.execute(args),


            "service": lambda: self.service_manager.execute(args),



            "schedule": lambda: self.scheduler.execute(args),



            "user": lambda: self.user_manager.execute(args),



            "log": lambda: self.logger.execute(args),

            "config": lambda: self.config_manager.execute(args),

            "grep": lambda: self.grep(args, None),



        }







        if name not in commands:



            print(f"Command not found: {name}")



            return False







        try:
            result = commands[name]()

            if result is None:
                success = True
            else:
                success = bool(result)

        except ValueError as error:
            print(f"Error: {error}")
            success = False

        except TypeError:
            print("Error: Invalid arguments.")
            success = False

        except FileNotFoundError:
            print("Error: File or directory not found.")
            success = False

        except PermissionError:
            print("Error: Permission denied.")
            success = False

        except Exception as error:
            print(f"Error: {error}")
            success = False

        self.log_action(command, success)







        if background and success:



            print("[Background process started]")







        return success







    def expand_variables(self, command):







        variables = self.environment.get_all()







        for name, value in variables.items():



            command = command.replace(



                f"${name}",



                str(value)



            )







        command = command.replace(



            "$USER",



            self.user["username"]



        )







        return command







    def expand_command_substitution(self, command):







        while "$(" in command:







            start = command.rfind("$(")







            depth = 0



            end = None







            for index in range(start + 1, len(command)):







                if command[index] == "(":



                    depth += 1







                elif command[index] == ")":



                    depth -= 1







                    if depth == 0:



                        end = index



                        break







            if end is None:



                print("Syntax error: unmatched $().")



                return command







            inner_command = command[



                start + 2:end



            ].strip()







            if not inner_command:



                return command







            output = self.capture_command(



                inner_command



            )







            command = (



                command[:start]



                + output



                + command[end + 1:]



            )







        return command







    def capture_command(self, command):







        try:



            args = shlex.split(command)



        except ValueError:



            return ""







        if not args:



            return ""







        name = args[0]



        args = args[1:]







        if name == "whoami":



            return self.user["username"]







        if name == "pwd":



            return self.filesystem.display_path()







        if name == "echo":



            return " ".join(args)







        if name == "date":



            return datetime.now().strftime(



                "%Y-%m-%d"



            )







        if name == "time":



            return datetime.now().strftime(



                "%H:%M:%S"



            )







        if name == "hostname":



            return socket.gethostname()







        if name == "uname":



            return platform.system()







        if name == "get" and len(args) == 1:



            success, value = self.environment.get(



                args[0]



            )







            if success:



                return str(value)







            return ""







        if name == "cat" and len(args) == 1:



            success, value = self.filesystem.read_file(



                args[0]



            )







            if success:



                return value







            return ""







        return ""







    def execute_pipe(self, command):







        parts = command.split("|")







        if len(parts) < 2:



            return False







        input_text = None



        success = True







        for part in parts:







            part = part.strip()







            try:



                args = shlex.split(part)



            except ValueError as error:



                print(f"Syntax error: {error}")



                return False







            if not args:



                continue







            name = args[0]



            args = args[1:]







            if name == "grep":



                success = self.grep(



                    args,



                    input_text



                )







                if input_text is None:



                    input_text = ""







                continue







            if name == "echo":



                input_text = " ".join(args)



                print(input_text)



                success = True



                continue







            if name == "cat" and len(args) == 1:







                file_success, result = (



                    self.filesystem.read_file(



                        args[0]



                    )



                )







                if not file_success:



                    print(result)



                    return False







                input_text = result



                print(input_text)



                success = True



                continue







            if name in ("ifconfig", "netstat", "ping"):



                try:

                    if name == "ifconfig":

                        network_command = ["ifconfig"]



                    elif name == "netstat":

                        network_command = ["netstat", "-an"]



                    else:

                        if len(args) < 1 or len(args) > 2:

                            print("Usage: ping <host> [count]")

                            return False



                        host = args[0]

                        count = 4



                        if len(args) == 2:

                            try:

                                count = int(args[1])

                            except ValueError:

                                print("Invalid count.")

                                return False



                            if count <= 0 or count > 10:

                                print("Count must be between 1 and 10.")

                                return False



                        network_command = ["ping", "-c", str(count), host]



                    result = subprocess.run(

                        network_command,

                        capture_output=True,

                        text=True

                    )



                    input_text = result.stdout

                    success = result.returncode == 0



                    if result.stderr.strip() and not input_text:

                        print(result.stderr.strip())



                    continue



                except FileNotFoundError:

                    print(f"{name} command not available.")

                    return False



                except Exception as error:

                    print(f"Network command failed: {error}")

                    return False



            print(



                f"Command '{name}' cannot be used in a pipe."



            )



            return False







        return success







    def handle_redirection(self, command):







        if ">>" in command:







            parts = command.split(">>", 1)







            left = parts[0].strip()



            right = parts[1].strip()







            if not right:



                print("Redirection file required.")



                return None







            try:



                filename = shlex.split(right)[0]



            except (ValueError, IndexError):



                print("Invalid redirection.")



                return None







            return left, "append", filename







        if ">" in command:







            parts = command.split(">", 1)







            left = parts[0].strip()



            right = parts[1].strip()







            if not right:



                print("Redirection file required.")



                return None







            try:



                filename = shlex.split(right)[0]



            except (ValueError, IndexError):



                print("Invalid redirection.")



                return None







            return left, "write", filename







        return None







    def execute_redirected(



        self,



        command,



        redirect_type,



        filename



    ):







        output = self.capture_command(command)







        if command.startswith("echo "):







            output = command[5:]







        elif command == "whoami":







            output = self.user["username"]







        elif command == "pwd":







            output = self.filesystem.display_path()







        elif command == "date":







            output = datetime.now().strftime(



                "%Y-%m-%d"



            )







        elif command == "time":







            output = datetime.now().strftime(



                "%H:%M:%S"



            )







        elif command == "hostname":







            output = socket.gethostname()







        elif command == "uname":







            output = platform.system()







        elif command.startswith("cat "):







            try:



                args = shlex.split(command)



            except ValueError:



                return False







            if len(args) != 2:



                return False







            success, output = (



                self.filesystem.read_file(



                    args[1]



                )



            )







            if not success:



                print(output)



                return False







        if redirect_type == "write":







            success, message = (



                self.filesystem.create_file(



                    filename,



                    output



                )



            )







            if not success:







                existing, _ = (



                    self.filesystem.read_file(



                        filename



                    )



                )







                if existing:







                    success, message = (



                        self.filesystem.write_file(



                            filename,



                            output



                        )



                    )







                else:



                    print(message)



                    return False







        else:







            success, existing = (



                self.filesystem.read_file(



                    filename



                )



            )







            if success:







                content = existing + output







                success, message = (



                    self.filesystem.write_file(



                        filename,



                        content



                    )



                )







            else:







                success, message = (



                    self.filesystem.create_file(



                        filename,



                        output



                    )



                )







        if not success:



            print(message)



            return False







        return True







    def echo(self, args):







        print(" ".join(args))







        return True







    def pwd(self):







        print(



            self.filesystem.display_path()



        )







        return True







    def whoami(self):







        print(



            self.user["username"]



        )







        return True







    def clear(self):







        os.system("clear")







        return True







    def exit(self):







        self.running = False







        return True







    def sysinfo(self):







        print()



        print("PyOS System Information")



        print("-----------------------")



        print(f"OS        : {platform.system()}")



        print(f"Release   : {platform.release()}")



        print(f"Machine   : {platform.machine()}")



        print(f"Python    : {platform.python_version()}")



        print(f"User      : {self.user['username']}")



        print()







        return True







    def date(self):







        print(



            datetime.now().strftime(



                "%Y-%m-%d"



            )



        )







        return True







    def time(self):







        print(



            datetime.now().strftime(



                "%H:%M:%S"



            )



        )







        return True







    def hostname(self):







        print(



            socket.gethostname()



        )







        return True







    def uname(self):







        print(



            platform.system()



        )







        return True



    def ping(self, args):







        if len(args) < 1 or len(args) > 2:



            print("Usage: ping <host> [count]")



            return False







        host = args[0]







        count = 4







        if len(args) == 2:



            try:



                count = int(args[1])



            except ValueError:



                print("Invalid count.")



                return False







        if count <= 0 or count > 10:



            print("Count must be between 1 and 10.")



            return False







        try:



            result = subprocess.run(



            [



                "ping",



                "-c",



                str(count),



                host



            ],



            capture_output=True,



            text=True



            )







            output = result.stdout.strip()







            if output:



                print(output)







            if result.stderr.strip():



                print(result.stderr.strip())







            return result.returncode == 0







        except FileNotFoundError:



            print("ping command not available.")



            return False







        except Exception as error:



            print(f"Ping failed: {error}")



            return False



    def ifconfig(self):







        try:







            result = subprocess.run(



                ["ifconfig"],



                capture_output=True,



                text=True



            )







            if result.stdout.strip():



                print(result.stdout.strip())







            if result.stderr.strip():



                print(result.stderr.strip())







            return result.returncode == 0







        except FileNotFoundError:







            print("ifconfig command not available.")



            return False







        except Exception as error:







            print(f"Network information unavailable: {error}")



            return False







    def netstat(self):







        try:







            result = subprocess.run(



                ["netstat", "-an"],



                capture_output=True,



                text=True



            )







            if result.stdout.strip():



                print(result.stdout.strip())







            if result.stderr.strip():



                print(result.stderr.strip())







            return result.returncode == 0







        except FileNotFoundError:







            print("netstat command not available.")



            return False







        except Exception as error:







            print(f"Network information unavailable: {error}")



            return False



    def uptime(self):







        try:







            result = subprocess.run(



                ["uptime"],



                capture_output=True,



                text=True



            )







            print(result.stdout.strip())







        except Exception:







            print(



                "Uptime information unavailable."



            )







        return True







    def grep(self, args, input_text):







        if len(args) < 1:







            print(



                "Usage: grep <pattern> [file]"



            )







            return False







        pattern = args[0]







        if input_text is not None:







            text = input_text







        elif len(args) == 2:







            success, result = (



                self.filesystem.read_file(



                    args[1]



                )



            )







            if not success:







                print(result)







                return False







            text = result







        else:







            print(



                "Usage: grep <pattern> [file]"



            )







            return False







        found = False







        for line in text.splitlines():







            if pattern in line:







                print(line)







                found = True







        return found







    def adduser(self, args):







        if not self.user["is_admin"]:







            print("Permission denied.")







            return False







        if len(args) != 1:







            print(



                "Usage: adduser <username>"



            )







            return False







        username = args[0]







        if not username.isidentifier():







            print("Invalid username.")







            return False







        password = getpass(



            "Enter password: "



        )







        confirm = getpass(



            "Confirm password: "



        )







        if password != confirm:







            print(



                "Passwords do not match."



            )







            return False







        if len(password) < 4:







            print(



                "Password must be at least 4 characters."



            )







            return False







        success = create_user(



            username,



            password,



            False



        )







        if not success:







            print(



                "Username already exists."



            )







            return False







        user_home = (



            self.filesystem.base_path



            / "home"



            / username



        )







        user_home.mkdir(



            parents=True,



            exist_ok=True



        )







        print(



            "User created successfully."



        )







        return True







    def users(self):







        users = get_all_users()







        if not users:







            print("No users found.")







            return True







        print()







        for user in users:







            username = user[1]







            account_type = (



                "Administrator"



                if user[2]



                else "Standard User"



            )







            print(



                f"{username} ({account_type})"



            )







        print()







        return True







    def help(self):
        print()
        print("========================================")
        print("             PyOS Help")
        print("========================================")

        print()
        print("General:")
        print("  help                 Show available commands")
        print("  clear                Clear the terminal")
        print("  echo <text>          Display text")
        print("  pwd                  Show current directory")
        print("  whoami               Show current username")
        print("  exit                 Exit PyOS")

        print()
        print("Filesystem:")
        print("  ls [path]            List files and directories")
        print("  cd <path>            Change directory")
        print("  mkdir <name>         Create a directory")
        print("  rmdir <name>         Remove an empty directory")
        print("  touch <name>         Create a file")
        print("  write <file> <text>  Write text to a file")
        print("  cat <file>           Display file contents")
        print("  rm <file>            Remove a file")
        print("  chmod <mode> <file>  Change permissions")
        print("  permissions <file>   Show file permissions")
        print("  stat <file>          Show file metadata")

        print()
        print("Process Management:")
        print("  ps                   Show all processes")
        print("  process <pid>        Show process details")
        print("  start <name>         Start a process")
        print("  kill <pid>           Terminate a process")
        print("  jobs                 Show background jobs")
        print("  fg <pid>             Move process to foreground")
        print("  bg <pid>             Move process to background")

        print()
        print("System:")
        print("  sysinfo              Show system information")
        print("  uname                Show PyOS kernel information")
        print("  hostname             Show system hostname")
        print("  uptime               Show system uptime")
        print("  date                 Show current date")
        print("  time                 Show current time")

        print()
        print("Networking:")
        print("  ping <host> [count]  Test network connectivity")
        print("  ifconfig             Show network interfaces")
        print("  netstat              Show network connections")

        print()
        print("Package Manager:")
        print("  pkg list             List available packages")
        print("  pkg installed        List installed packages")
        print("  pkg install <name>   Install a package")
        print("  pkg remove <name>    Remove a package")
        print("  pkg info <name>      Show package information")

        print()
        print("Service Manager:")
        print("  service list         List all services")
        print("  service status <n>   Show service status")
        print("  service start <n>    Start a service")
        print("  service stop <n>     Stop a service")
        print("  service restart <n>  Restart a service")

        print()
        print("Scheduler:")
        print("  schedule list        List scheduled tasks")
        print("  schedule add <n> <s> Schedule a task")
        print("  schedule remove <id> Remove a task")
        print("  schedule run <id>    Run a ready task")

        print()
        print("User Management:")
        print("  users                List all users")
        print("  adduser <username>   Create a new user")
        print("  user list            List all users")
        print("  user add <username>  Create a new user")
        print("  user delete <name>   Delete a user")
        print("  user passwd [name]   Change password")

        print()
        print("Configuration:")
        print("  config list           List configuration")
        print("  config get <key>      Get a configuration value")
        print("  config set <key> <v>  Set a configuration value")
        print("  config reset          Reset configuration")

        print()
        print("Logging:")
        print("  log show [limit]      Show system log")
        print("  log clear             Clear system log")

        print()
        print("History:")
        print("  history [limit]       Show command history")
        print("  clearhistory          Clear command history")

        print()
        print("Environment:")
        print("  env                   Show environment variables")
        print("  set <name> <value>    Set a variable")
        print("  get <name>            Get a variable")
        print("  unset <name>          Remove a variable")

        print()
        print("Text:")
        print("  grep <text>            Search text")

        print()
        print("Shell Operators:")
        print("  |                    Pipe output to another command")
        print("  >                    Write command output to a file")
        print("  >>                   Append command output to a file")
        print("  &&                   Run next command if successful")
        print("  ||                   Run next command if failed")
        print("  $(...)               Command substitution")
        print("  &                    Run a process in background")

        print()
        return True


    def env(self):







        variables = (



            self.environment.get_all()



        )







        if not variables:







            print(



                "No environment variables."



            )







            return True







        for name, value in variables.items():







            print(



                f"{name}={value}"



            )







        return True







    def set_variable(self, args):







        if len(args) != 1:







            print(



                "Usage: set <name>=<value>"



            )







            return False







        expression = args[0]







        if "=" not in expression:







            print(



                "Usage: set <name>=<value>"



            )







            return False







        name, value = expression.split(



            "=",



            1



        )







        name = name.strip()







        success, message = (



            self.environment.set(



                name,



                value



            )



        )







        print(message)







        return success







    def get_variable(self, args):







        if len(args) != 1:







            print(



                "Usage: get <name>"



            )







            return False







        success, result = (



            self.environment.get(



                args[0]



            )



        )







        print(result)







        return success







    def unset_variable(self, args):







        if len(args) != 1:







            print(



                "Usage: unset <name>"



            )







            return False







        success, message = (



            self.environment.unset(



                args[0]



            )



        )







        print(message)







        return success







    def ps(self):







        processes = (



            self.process_manager.get_processes()



        )







        print()







        print(



            f"{'PID':<8}"



            f"{'USER':<12}"



            f"{'NAME':<16}"



            f"{'STATUS'}"



        )







        print("-" * 55)







        for process in processes:







            print(



                f"{process['pid']:<8}"



                f"{process['user']:<12}"



                f"{process['name']:<16}"



                f"{process['status']}"



            )







        print()







        return True







    def jobs(self):







        processes = (



            self.process_manager



            .get_running_processes()



        )







        if not processes:







            print(



                "No running jobs."



            )







            return True







        print()







        print(



            f"{'PID':<8}"



            f"{'USER':<12}"



            f"{'NAME':<16}"



            f"{'STATUS'}"



        )







        print("-" * 55)







        for process in processes:







            print(



                f"{process['pid']:<8}"



                f"{process['user']:<12}"



                f"{process['name']:<16}"



                f"{process['status']}"



            )







        print()







        return True



    def fg(self, args):







        if len(args) != 1:



            print("Usage: fg <pid>")



            return False







        process = self.process_manager.get_process(args[0])







        if process is None:



            print("Process not found.")



            return False







        if process["status"] == "TERMINATED":



            print("Process is already terminated.")



            return False







        process["status"] = "FOREGROUND"







        print(



        f"Process {process['pid']} "



        f"({process['name']}) moved to foreground."



        )







        return True



    def bg(self, args):







        if len(args) != 1:



            print("Usage: bg <pid>")



            return False







        process = self.process_manager.get_process(args[0])







        if process is None:



            print("Process not found.")



            return False







        if process["status"] == "TERMINATED":



            print("Process is already terminated.")



            return False







        process["status"] = "RUNNING"







        print(



            f"Process {process['pid']} "



            f"({process['name']}) moved to background."



        )







        return True



    def start(self, args):







        if len(args) != 1:







            print(



                "Usage: start <process>"



            )







            return False







        name = args[0]







        success, result = (



            self.process_manager.create_process(



                self.user["username"],



                name



            )



        )







        if success:







            print(



                f"Process started with PID {result}."



            )







        else:







            print(result)







        return success







    def kill(self, args):







        if len(args) != 1:







            print(



                "Usage: kill <pid>"



            )







            return False







        success, message = (



            self.process_manager.kill_process(



                args[0],



                self.user["username"],



                self.user["is_admin"]



            )



        )







        print(message)







        return success







    def process(self, args):







        if len(args) != 1:







            print(



                "Usage: process <pid>"



            )







            return False







        process = (



            self.process_manager.get_process(



                args[0]



            )



        )







        if process is None:







            print(



                "Process not found."



            )







            return False







        print()







        print(



            f"PID     : {process['pid']}"



        )







        print(



            f"User    : {process['user']}"



        )







        print(



            f"Name    : {process['name']}"



        )







        print(



            f"Status  : {process['status']}"



        )







        print(



            f"Started : "



            f"{process['started'].strftime('%Y-%m-%d %H:%M:%S')}"



        )







        print()







        return True







    def show_history(self, args):







        if len(args) > 1:







            print(



                "Usage: history [number]"



            )







            return False







        if len(args) == 1:







            try:







                limit = int(args[0])







                if limit <= 0:







                    print(



                        "Number must be greater than 0."



                    )







                    return False







            except ValueError:







                print(



                    "Invalid number."



                )







                return False







        else:







            limit = None







        commands = self.history.get(



            limit



        )







        if not commands:







            print(



                "No command history."



            )







            return True







        start_number = (



            len(self.history.commands)



            - len(commands)



            + 1



        )







        print()







        for index, command in enumerate(



            commands,



            start=start_number



        ):







            print(



                f"{index:4}  {command}"



            )







        print()







        return True







    def clear_history(self):







        self.history.clear()







        print(



            "Command history cleared."



        )







        return True







    def ls(self, args):







        if len(args) > 1:







            print(



                "Usage: ls [directory]"



            )







            return False







        if args:







            path = args[0]







            target = (



                self.filesystem.resolve_path(



                    path



                )



            )







            if target is None:







                print(



                    "Permission denied."



                )







                return False







            if not target.exists():







                print(



                    "Directory does not exist."



                )







                return False







            if not target.is_dir():







                print(



                    "Not a directory."



                )







                return False







            items = (



                self.filesystem.list_directory(



                    path



                )



            )







        else:







            items = (



                self.filesystem.list_directory()



            )







        for item in items:







            if item.is_dir():







                print(



                    f"{item.name}/"



                )







            else:







                print(item.name)







        return True







    def mkdir(self, args):







        if len(args) != 1:







            print(



                "Usage: mkdir <directory>"



            )







            return False







        success, message = (



            self.filesystem.make_directory(



                args[0]



            )



        )







        print(message)







        return success







    def cd(self, args):







        if len(args) != 1:







            print(



                "Usage: cd <directory>"



            )







            return False







        success, message = (



            self.filesystem.change_directory(



                args[0]



            )



        )







        if not success:







            print(message)







        return success







    def rmdir(self, args):







        if len(args) != 1:







            print(



                "Usage: rmdir <directory>"



            )







            return False







        success, message = (



            self.filesystem.remove_directory(



                args[0]



            )



        )







        print(message)







        return success





    def stat(self, args):

        if len(args) != 1:

            print("Usage: stat <file>")

            return False



        name = args[0]



        path = self.filesystem.resolve_path(name)



        if path is None:

            print("Permission denied.")

            return False



        if not path.exists():

            print("File or directory does not exist.")

            return False



        permission = self.filesystem.get_permission(path)



        file_type = "DIRECTORY" if path.is_dir() else "FILE"



        size = path.stat().st_size

        mode = permission["mode"]

        owner = permission["owner"]



        modified = datetime.fromtimestamp(

            path.stat().st_mtime

        ).strftime("%Y-%m-%d %H:%M:%S")



        created = datetime.fromtimestamp(

            path.stat().st_ctime

        ).strftime("%Y-%m-%d %H:%M:%S")



        print()

        print("==============================")

        print("        File Metadata")

        print("==============================")

        print()

        print(f"Name:        {path.name}")

        print(f"Type:        {file_type}")

        print(f"Size:        {size} bytes")

        print(f"Owner:       {owner}")

        print(f"Permissions: {mode}")

        print(f"Path:        {path}")

        print(f"Created:     {created}")

        print(f"Modified:    {modified}")

        print()



        return True

    def touch(self, args):







        if len(args) != 1:







            print(



                "Usage: touch <filename>"



            )







            return False







        success, message = (



            self.filesystem.create_file(



                args[0]



            )



        )







        print(message)







        return success







    def write(self, args):







        if len(args) < 2:







            print(



                "Usage: write <filename> <content>"



            )







            return False







        filename = args[0]







        content = " ".join(



            args[1:]



        )







        success, message = (



            self.filesystem.write_file(



                filename,



                content



            )



        )







        print(message)







        return success







    def rm(self, args):







        if len(args) != 1:







            print(



                "Usage: rm <filename>"



            )







            return False







        success, message = (



            self.filesystem.remove_file(



                args[0]



            )



        )







        print(message)







        return success







    def cat(self, args):







        if len(args) != 1:







            print(



                "Usage: cat <filename>"



            )







            return False







        success, result = (



            self.filesystem.read_file(



                args[0]



            )



        )







        print(result)







        return success







    def chmod(self, args):







        if len(args) != 2:







            print(



                "Usage: chmod <mode> <file>"



            )







            return False







        mode = args[0]



        filename = args[1]







        success, message = (



            self.filesystem.chmod(



                mode,



                filename



            )



        )







        print(message)







        return success







    def permissions(self, args):







        if len(args) != 1:







            print(



                "Usage: permissions <file>"



            )







            return False







        filename = args[0]







        success, result = (



            self.filesystem.get_mode(



                filename



            )



        )







        print(result)







        return success
