
import unittest
from pathlib import Path


class TestEmailAutomationProject(unittest.TestCase):

    def test_main_file_exists(self):
        self.assertTrue(Path("main.py").is_file())

    def test_automation_file_exists(self):
        self.assertTrue(Path("src/automation.py").is_file())

    def test_email_template_exists(self):
        self.assertTrue(Path("templates/email.txt").is_file())

    def test_contacts_file_exists(self):
        self.assertTrue(Path("data/contacts.csv").is_file())

    def test_reminders_file_exists(self):
        self.assertTrue(Path("data/reminders.csv").is_file())

    def test_readme_exists(self):
        self.assertTrue(Path("README.md").is_file())


if __name__ == "__main__":
    unittest.main()
