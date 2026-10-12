from pathlib import Path
import time

from System.core.database import initialize_database
from System.core.config_manager import ConfigManager


class BootManager:

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[2]
        self.filesystem_dir = self.base_dir / "Filesystem"
        self.data_dir = self.base_dir / "System" / "data"

    def show_header(self):
        print()
        print("================================")
        print("          PyOS BOOT")
        print("================================")
        print()

    def step(self, message):
        print(f"[ OK ] {message}")

    def initialize_directories(self):
        self.filesystem_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        (self.filesystem_dir / "home").mkdir(
            parents=True,
            exist_ok=True
        )

        self.data_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def boot(self):
        self.show_header()

        try:
            self.initialize_directories()
            self.step("Preparing filesystem")

            initialize_database()
            self.step("Initializing database")

            ConfigManager(
                "system",
                True
            )
            self.step("Loading system configuration")

            self.step("Loading process manager")
            self.step("Loading service manager")
            self.step("Loading scheduler")
            self.step("Loading logger")
            self.step("Loading network subsystem")

            print()
            print("Boot completed successfully.")
            print()
            print("Starting login manager...")
            print()

            return True

        except Exception as error:
            print()
            print("[ FAIL ] PyOS boot failed.")
            print(f"Error: {error}")
            print()

            return False