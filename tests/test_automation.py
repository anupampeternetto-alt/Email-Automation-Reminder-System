
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

    def test_email_personalization(self):
        from src.automation import generate_email

        message = generate_email(
            name="Test Student",
            event="Python Project Review",
            due_at="2026-12-01 10:00"
        )

        self.assertIn("Test Student", message)
        self.assertIn("Python Project Review", message)
        self.assertIn("2026-12-01 10:00", message)

    def test_email_dry_run(self):
        from unittest.mock import patch
        from src.automation import send_email

        with patch("smtplib.SMTP") as mock_smtp:
            result = send_email(
                recipient="student@example.com",
                subject="Test Reminder",
                body="This is a test.",
                dry_run=True
            )

            self.assertEqual(result, "SIMULATED")
            mock_smtp.assert_not_called()

    def test_duplicate_reminders_are_skipped(self):
        import io
        from contextlib import redirect_stdout
        from unittest.mock import patch
        import pandas as pd
        from src.automation import simulate_due_emails

        contacts = pd.DataFrame([
            {
                "contact_id": "C001",
                "name": "Test Student",
                "email": "student@example.com"
            }
        ])

        reminders = pd.DataFrame([
            {
                "reminder_id": "R001",
                "contact_id": "C001",
                "event": "Project Review",
                "due_at": "2020-01-01 10:00"
            }
        ])

        class FakeReportPath:
            def exists(self):
                return True

            def open(self, *args, **kwargs):
                return io.StringIO(
                    "reminder_id,email,status,processed_at,error\n"
                    "R001,student@example.com,SIMULATED,2020-01-01T10:00:00,\n"
                )

        output = io.StringIO()

        with patch(
            "src.automation.load_data",
            return_value=(contacts, reminders)
        ), patch(
            "src.automation.Path",
            return_value=FakeReportPath()
        ), patch(
            "src.automation.send_email"
        ) as mock_send, redirect_stdout(output):
            simulate_due_emails()

        self.assertIn("SKIPPED: R001", output.getvalue())
        mock_send.assert_not_called()


if __name__ == "__main__":
    unittest.main()
