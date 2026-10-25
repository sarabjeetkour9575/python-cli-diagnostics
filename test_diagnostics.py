import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class TestDiagnostics(unittest.TestCase):
    def test_success(self):
        result = main.run_diagnostics()
        self.assertTrue(result["python_version"])
        self.assertTrue(result["operating_system"])
        self.assertIn("disk_space", result)
        self.assertIn("environment_variables", result)
        self.assertIn("developer_tools", result)
        self.assertTrue(result["configuration"]["valid"])

    def test_missing_dependency(self):
        # Simulate Git not being installed/available on PATH.
        with patch("main.shutil.which", return_value=None):
            result = main.run_diagnostics()
        self.assertFalse(result["developer_tools"]["git_available"])

    def test_malformed_configuration_path(self):
        result = main.run_diagnostics(
            config_path="definitely_missing_config_987654.json"
        )
        self.assertFalse(result["configuration"]["valid"])
        self.assertIn("error", result["configuration"])

    def test_valid_configuration_path(self):
        with tempfile.TemporaryDirectory() as folder:
            config_file = Path(folder) / "config.json"
            config_file.write_text("{}", encoding="utf-8")
            result = main.run_diagnostics(config_path=str(config_file))
        self.assertTrue(result["configuration"]["valid"])

    def test_disk_usage_error_is_handled(self):
        with patch(
            "main.shutil.disk_usage",
            side_effect=FileNotFoundError("Path not found"),
        ):
            result = main.run_diagnostics()
        self.assertIn("error", result["disk_space"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
