import unittest
import tempfile
from pathlib import Path

from System.core.database import initialize_database, create_user, get_user
from System.core.filesystem import FileSystem
from System.core.environment import EnvironmentManager
from System.core.process import ProcessManager
from System.core.package_manager import PackageManager
from System.core.service_manager import ServiceManager


class TestDatabase(unittest.TestCase):

    def test_database_initialization(self):
        initialize_database()
        self.assertTrue(True)

    def test_create_user(self):
        username = "test_auto_user"
        password = "test123"

        create_user(username, password)

        user = get_user(username)

        self.assertIsNotNone(user)
        self.assertEqual(user[1], username)


class TestFileSystem(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base_path = Path(self.temp_dir.name)

        self.fs = FileSystem(
            base_path,
            "root",
            True
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_file(self):
        success, message = self.fs.create_file(
            "test.txt",
            "Hello PyOS"
        )

        self.assertTrue(success)

        success, content = self.fs.read_file("test.txt")

        self.assertTrue(success)
        self.assertEqual(content, "Hello PyOS")

    def test_write_file(self):
        self.fs.create_file(
            "test.txt",
            "Hello"
        )

        success, message = self.fs.write_file(
            "test.txt",
            "Updated"
        )

        self.assertTrue(success)

        success, content = self.fs.read_file(
            "test.txt"
        )

        self.assertTrue(success)
        self.assertEqual(content, "Updated")

    def test_create_directory(self):
        success, message = self.fs.make_directory(
            "testdir"
        )

        self.assertTrue(success)

        path = self.fs.resolve_path(
            "testdir"
        )

        self.assertTrue(path.exists())
        self.assertTrue(path.is_dir())


class TestEnvironment(unittest.TestCase):

    def test_environment_variable(self):

        env = EnvironmentManager(
            "test_environment_user"
        )

        success, message = env.set(
            "TEST_VARIABLE",
            "Hello"
        )

        self.assertTrue(success)

        success, value = env.get(
            "TEST_VARIABLE"
        )

        self.assertTrue(success)
        self.assertEqual(value, "Hello")

        success, message = env.unset(
            "TEST_VARIABLE"
        )

        self.assertTrue(success)


class TestProcessManager(unittest.TestCase):

    def setUp(self):
        self.process_manager = ProcessManager()

    def test_create_process(self):

        success, pid = self.process_manager.create_process(
            "root",
            "calculator"
        )

        self.assertTrue(success)
        self.assertEqual(pid, 2)

    def test_kill_process(self):

        success, pid = self.process_manager.create_process(
            "root",
            "editor"
        )

        self.assertTrue(success)

        success, message = self.process_manager.kill_process(
            pid,
            "root"
        )

        self.assertTrue(success)
        self.assertEqual(
            message,
            "Process terminated."
        )

    def test_shell_cannot_be_killed(self):

        success, message = self.process_manager.kill_process(
            1,
            "root"
        )

        self.assertFalse(success)

        self.assertEqual(
            message,
            "Cannot terminate shell process."
        )


class TestPackageManager(unittest.TestCase):

    def test_available_packages(self):

        manager = PackageManager(
            "root",
            True
        )

        self.assertIn(
            "calculator",
            manager.packages
        )

        self.assertIn(
            "editor",
            manager.packages
        )


class TestServiceManager(unittest.TestCase):

    def setUp(self):
        self.manager = ServiceManager(
            "root",
            True
        )

        self.manager.services["scheduler"]["status"] = "STOPPED"
        self.manager.save()

    def test_list_services(self):

        self.assertIn(
            "network",
            self.manager.services
        )

        self.assertIn(
            "database",
            self.manager.services
        )

        self.assertIn(
            "logger",
            self.manager.services
        )

        self.assertIn(
            "scheduler",
            self.manager.services
        )

        result = self.manager.list_services()

        self.assertTrue(result)

    def test_service_status(self):

        result = self.manager.status(
            "scheduler"
        )

        self.assertTrue(result)

        self.assertIn(
            "scheduler",
            self.manager.services
        )

        self.assertIn(
            self.manager.services["scheduler"]["status"],
            ["RUNNING", "STOPPED"]
        )

    def test_start_service(self):

        self.manager.stop(
            "scheduler"
        )

        result = self.manager.start(
            "scheduler"
        )

        self.assertTrue(result)

        self.assertEqual(
            self.manager.services["scheduler"]["status"],
            "RUNNING"
        )

    def test_stop_service(self):

        self.manager.start(
            "scheduler"
        )

        result = self.manager.stop(
            "scheduler"
        )

        self.assertTrue(result)

        self.assertEqual(
            self.manager.services["scheduler"]["status"],
            "STOPPED"
        )

    def test_restart_service(self):

        self.manager.stop(
            "scheduler"
        )

        result = self.manager.restart(
            "scheduler"
        )

        self.assertTrue(result)

        self.assertEqual(
            self.manager.services["scheduler"]["status"],
            "RUNNING"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)