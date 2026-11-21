
from datetime import datetime
import logging

from app.database import SessionLocal
from app.models import Reminder
from src.automation import send_email

logging.basicConfig(level=logging.INFO)


def check_database_reminders():
    """Process due SQLite reminders in safe simulation mode."""
    db = SessionLocal()

    try:
        reminders = (
            db.query(Reminder)
            .filter(Reminder.status == "PENDING")
            .all()
        )

        for reminder in reminders:
            if reminder.due_at > datetime.now():
                continue

            contact = reminder.contact

            if not contact or not contact.email:
                logging.warning(
                    "Missing contact for reminder %s",
                    reminder.id
                )
                continue

            subject = f"Reminder: {reminder.event}"
            body = (
                f"Hello {contact.name},\n\n"
                f"This is a reminder for {reminder.event}.\n"
                f"Due date: {reminder.due_at}\n\n"
                "Best regards,\n"
                "Email Automation System"
            )

            result = send_email(
                recipient=contact.email,
                subject=subject,
                body=body,
                dry_run=True
            )

            if result == "SIMULATED":
                logging.info(
                    "Simulated reminder %s for %s",
                    reminder.id,
                    contact.email
                )

    finally:
        db.close()


if __name__ == "__main__":
    check_database_reminders()
import time

if __name__ == "__main__":
    print("Automatic reminder scheduler started.")
    print("Checking reminders every 60 seconds.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            check_database_reminders()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")