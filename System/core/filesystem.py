from pathlib import Path
import json


class FileSystem:

    def __init__(self, base_path, username, is_admin=False):
        self.base_path = Path(base_path).resolve()
        self.username = username
        self.is_admin = is_admin

        self.user_home = self.base_path / "home" / username
        self.user_home.mkdir(parents=True, exist_ok=True)

        self.current_path = self.user_home

        self.permission_file = self.base_path / ".permissions.json"

        if not self.permission_file.exists():
            self.permission_file.write_text("{}")

        self.permissions = self.load_permissions()

        self.get_permission(self.user_home)

    def load_permissions(self):
        try:
            return json.loads(self.permission_file.read_text())
        except Exception:
            return {}

    def save_permissions(self):
        self.permission_file.write_text(
            json.dumps(self.permissions, indent=4)
        )

    def relative_path(self):
        try:
            return self.current_path.relative_to(self.user_home)
        except ValueError:
            return self.current_path.relative_to(self.base_path)

    def display_path(self):
        try:
            relative = self.current_path.relative_to(self.user_home)

            if str(relative) == ".":
                return f"/home/{self.username}"

            return f"/home/{self.username}/{relative}"

        except ValueError:
            relative = self.current_path.relative_to(self.base_path)
            return "/" + str(relative)

    def resolve_path(self, path):
        if not path:
            return None

        path = str(path)

        if path == "~":
            target = self.user_home

        elif path.startswith("/"):

            if path == "/":
                return None

            if path == f"/home/{self.username}":
                target = self.user_home

            elif path.startswith(f"/home/{self.username}/"):
                relative = path[len(f"/home/{self.username}/"):]
                target = self.user_home / relative

            elif self.is_admin and path.startswith("/home/"):
                relative = path[len("/home/"):]
                target = self.base_path / "home" / relative

            else:
                return None

        else:
            target = self.current_path / path

        target = target.resolve()

        if not self.is_admin:
            if not self.is_inside_home(target):
                return None
        else:
            if not self.is_inside_filesystem(target):
                return None

        return target

    def get_key(self, path):
        return str(path.relative_to(self.base_path))

    def get_permission(self, path):
        key = self.get_key(path)

        if key not in self.permissions:

            owner = self.username

            try:
                relative = path.relative_to(self.base_path)
                parts = relative.parts

                if len(parts) >= 2 and parts[0] == "home":
                    owner = parts[1]
            except ValueError:
                pass

            if path.is_dir():
                mode = 755
            else:
                mode = 644

            self.permissions[key] = {
                "owner": owner,
                "mode": mode
            }

            self.save_permissions()

        return self.permissions[key]

    def can_read(self, path):
        if self.is_admin:
            return True

        permission = self.get_permission(path)

        mode = int(permission["mode"])

        owner = permission["owner"]

        if owner == self.username:
            permissions = (mode // 100) % 10
        else:
            permissions = mode % 10

        return (permissions & 4) != 0

    def can_write(self, path):
        if self.is_admin:
            return True

        permission = self.get_permission(path)

        mode = int(permission["mode"])

        owner = permission["owner"]

        if owner == self.username:
            permissions = (mode // 100) % 10
        else:
            permissions = mode % 10

        return (permissions & 2) != 0

    def can_execute(self, path):
        if self.is_admin:
            return True

        permission = self.get_permission(path)

        mode = int(permission["mode"])

        owner = permission["owner"]

        if owner == self.username:
            permissions = (mode // 100) % 10
        else:
            permissions = mode % 10

        return (permissions & 1) != 0

    def list_directory(self, path=None):

        if path is None:
            target = self.current_path
        else:
            target = self.resolve_path(path)

        if target is None:
            return []

        if not target.exists():
            return []

        if not target.is_dir():
            return []

        if not self.can_read(target):
            return []

        return sorted(
            target.iterdir(),
            key=lambda item: item.name
        )

    def make_directory(self, name):

        if not self.valid_path(name):
            return False, "Invalid directory name."

        path = self.resolve_path(name)

        if path is None:
            return False, "Permission denied."

        if path.exists():
            return False, "Directory already exists."

        if not path.parent.exists():
            return False, "Parent directory does not exist."

        if not path.parent.is_dir():
            return False, "Parent is not a directory."

        if not self.can_write(path.parent):
            return False, "Permission denied."

        path.mkdir()

        key = self.get_key(path)

        self.permissions[key] = {
            "owner": self.username,
            "mode": 755
        }

        self.save_permissions()

        return True, "Directory created."

    def remove_directory(self, name):

        if not self.valid_path(name):
            return False, "Invalid directory name."

        path = self.resolve_path(name)

        if path is None:
            return False, "Permission denied."

        if not path.exists():
            return False, "Directory does not exist."

        if not path.is_dir():
            return False, "Not a directory."

        if path == self.user_home and not self.is_admin:
            return False, "Cannot remove home directory."

        if path == self.base_path / "home":
            return False, "Cannot remove home directory."

        if any(path.iterdir()):
            return False, "Directory is not empty."

        if not self.can_write(path.parent):
            return False, "Permission denied."

        path.rmdir()

        key = self.get_key(path)

        if key in self.permissions:
            del self.permissions[key]
            self.save_permissions()

        return True, "Directory removed."

    def change_directory(self, path):

        target = self.resolve_path(path)

        if target is None:
            return False, "Permission denied."

        if not target.exists():
            return False, "Directory does not exist."

        if not target.is_dir():
            return False, "Not a directory."

        if not self.can_read(target):
            return False, "Permission denied."

        self.current_path = target

        return True, "Directory changed."

    def create_file(self, name, content=""):

        if not self.valid_path(name):
            return False, "Invalid file name."

        path = self.resolve_path(name)

        if path is None:
            return False, "Permission denied."

        if path.exists():
            return False, "File already exists."

        if not path.parent.exists():
            return False, "Parent directory does not exist."

        if not path.parent.is_dir():
            return False, "Parent is not a directory."

        if not self.can_write(path.parent):
            return False, "Permission denied."

        path.write_text(content)

        key = self.get_key(path)

        self.permissions[key] = {
            "owner": self.username,
            "mode": 644
        }

        self.save_permissions()

        return True, "File created."

    def write_file(self, name, content):

        if not self.valid_path(name):
            return False, "Invalid file name."

        path = self.resolve_path(name)

        if path is None:
            return False, "Permission denied."

        if not path.exists():
            return False, "File does not exist."

        if not path.is_file():
            return False, "Not a file."

        if not self.can_write(path):
            return False, "Permission denied."

        path.write_text(content)

        return True, "File written."

    def remove_file(self, name):

        if not self.valid_path(name):
            return False, "Invalid file name."

        path = self.resolve_path(name)

        if path is None:
            return False, "Permission denied."

        if not path.exists():
            return False, "File does not exist."

        if not path.is_file():
            return False, "Not a file."

        if not self.can_write(path.parent):
            return False, "Permission denied."

        path.unlink()

        key = self.get_key(path)

        if key in self.permissions:
            del self.permissions[key]
            self.save_permissions()

        return True, "File removed."

    def read_file(self, name):

        if not self.valid_path(name):
            return False, "Invalid file name."

        path = self.resolve_path(name)

        if path is None:
            return False, "Permission denied."

        if not path.exists():
            return False, "File does not exist."

        if not path.is_file():
            return False, "Not a file."

        if not self.can_read(path):
            return False, "Permission denied."

        return True, path.read_text()

    def chmod(self, mode, name):

        if not self.valid_path(name):
            return False, "Invalid file name."

        path = self.resolve_path(name)

        if path is None:
            return False, "Permission denied."

        if not path.exists():
            return False, "File or directory does not exist."

        if not str(mode).isdigit():
            return False, "Invalid permission mode."

        mode = str(mode)

        if len(mode) != 3:
            return False, "Permission mode must have 3 digits."

        if any(int(digit) > 7 for digit in mode):
            return False, "Invalid permission mode."

        permission = self.get_permission(path)

        if not self.is_admin:
            if permission["owner"] != self.username:
                return False, "Permission denied."

        permission["mode"] = int(mode)

        key = self.get_key(path)

        self.permissions[key] = permission

        self.save_permissions()

        return True, "Permissions changed."

    def get_mode(self, name):

        if not self.valid_path(name):
            return False, "Invalid file name."

        path = self.resolve_path(name)

        if path is None:
            return False, "Permission denied."

        if not path.exists():
            return False, "File or directory does not exist."

        permission = self.get_permission(path)

        return True, str(permission["mode"])

    def valid_path(self, name):

        if not name:
            return False

        name = str(name)

        if "\\" in name:
            return False

        if "\0" in name:
            return False

        if name.startswith("/"):

            if name == f"/home/{self.username}":
                return True

            if name.startswith(f"/home/{self.username}/"):
                return True

            if self.is_admin and name.startswith("/home/"):
                return True

            return False

        parts = Path(name).parts

        for part in parts:

            if part == "":
                return False

            if "\0" in part:
                return False

        return True

    def is_inside_home(self, path):

        try:
            path.relative_to(self.user_home)
            return True
        except ValueError:
            return False

    def is_inside_filesystem(self, path):

        try:
            path.relative_to(self.base_path)
            return True
        except ValueError:
            return False