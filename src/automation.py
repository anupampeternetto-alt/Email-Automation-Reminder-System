
from pathlib import Path
from string import Template
import pandas as pd


def load_data():
    """Load contacts and reminders from CSV files."""
    contacts = pd.read_csv("data/contacts.csv")
    reminders = pd.read_csv("data/reminders.csv")
    return contacts, reminders


def generate_email(name, event, due_at):
    """Create a personalized email using the template."""
    template_path = Path("templates/email.txt")
    template_text = template_path.read_text(encoding="utf-8")

    template = Template(template_text)

    return template.substitute(
        name=name,
        event=event,
        due_at=due_at
    )


def preview_emails():
    """Generate email previews for all valid reminders."""
    contacts, reminders = load_data()

    merged = reminders.merge(
        contacts,
        on="contact_id",
        how="left",
        validate="many_to_one"
    )

    for _, row in merged.iterrows():
        if pd.isna(row["email"]):
            print(f"Missing contact for {row['reminder_id']}")
            continue

        email_body = generate_email(
            name=row["name"],
            event=row["event"],
            due_at=row["due_at"]
        )

        print("=" * 50)
        print(f"To: {row['email']}")
        print(email_body)
        print("STATUS: PREVIEW ONLY - NOT SENT")
        print("=" * 50)


if __name__ == "__main__":
    preview_emails()

from datetime import datetime
import schedule
import time


def check_due_reminders():
    """Check which reminders are due."""
    contacts, reminders = load_data()

    merged = reminders.merge(
        contacts,
        on="contact_id",
        how="left"
    )

    current_time = datetime.now()

    print(f"\nChecking reminders at: {current_time}")

    for _, row in merged.iterrows():
        reminder_time = datetime.strptime(
            row["due_at"],
            "%Y-%m-%d %H:%M"
        )

        if reminder_time <= current_time:
            print(
                f"DUE: {row['name']} - {row['event']}"
            )
        else:
            print(
                f"PENDING: {row['name']} - {row['event']}"
            )


def start_scheduler():
    """Check reminders every minute."""
    print("Reminder scheduler started...")
    print("Press Ctrl+C to stop.")

    check_due_reminders()

    schedule.every(1).minutes.do(
        check_due_reminders
    )

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")

import csv
import logging
from datetime import datetime
from pathlib import Path

# Create output folders if they do not exist.
Path("logs").mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def simulate_due_emails():
    """Simulate due reminders and save their status."""

    contacts, reminders = load_data()

    merged = reminders.merge(
        contacts,
        on="contact_id",
        how="left",
        validate="many_to_one"
    )

    report_path = Path("outputs/email_report.csv")
    processed_ids = set()

    # Read previous results to prevent duplicate simulation.
    if report_path.exists():
        with report_path.open(
            "r", newline="", encoding="utf-8"
        ) as file:
            for record in csv.DictReader(file):
                if record["status"] == "SIMULATED":
                    processed_ids.add(record["reminder_id"])

    new_report = []

    for _, row in merged.iterrows():
        reminder_id = str(row["reminder_id"])

        if reminder_id in processed_ids:
            print(f"SKIPPED: {reminder_id} already processed")
            continue

        try:
            reminder_time = datetime.strptime(
                str(row["due_at"]),
                "%Y-%m-%d %H:%M"
            )

            if reminder_time > datetime.now():
                print(f"PENDING: {reminder_id}")
                continue

            if pd.isna(row["email"]) or pd.isna(row["name"]):
                raise ValueError("Contact information missing")

            message = generate_email(
                name=row["name"],
                event=row["event"],
                due_at=row["due_at"]
            )

            subject_line, separator, email_body = message.partition("\n")

            if not separator or not subject_line.startswith("Subject: "):
                raise ValueError(
                    "Email template has no valid Subject line"
                )

            subject = subject_line.removeprefix("Subject: ").strip()

            status = send_email(
                recipient=str(row["email"]),
                subject=subject,
                body=email_body.strip(),
                dry_run=True
            )

            error = ""

   

        except Exception as exc:
            status = "FAILED"
            error = str(exc)

            print(f"FAILED: {reminder_id} - {error}")
            logging.error(
                "Reminder %s failed: %s",
                reminder_id, error
            )

        new_report.append({
            "reminder_id": reminder_id,
            "email": (
                "" if pd.isna(row["email"])
                else str(row["email"])
            ),
            "status": status,
            "processed_at": datetime.now().isoformat(
                timespec="seconds"
            ),
            "error": error
        })

    if new_report:
        with report_path.open(
            "a", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "reminder_id",
                    "email",
                    "status",
                    "processed_at",
                    "error"
                ]
            )

            if file.tell() == 0:
                writer.writeheader()

            writer.writerows(new_report)

    print("\nReport:", report_path)
    print("Simulation completed. No emails were sent.")

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


def send_email(recipient, subject, body, dry_run=True):
    """Preview or send an email through SMTP."""

    if dry_run:
        print(f"\nDRY RUN - To: {recipient}")
        print(f"Subject: {subject}")
        print(body)
        print("STATUS: SIMULATED - NOT SENT")
        return "SIMULATED"

    load_dotenv()

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_host, smtp_user, smtp_password]):
        raise ValueError(
            "Missing SMTP configuration. Check your .env file."
        )

    message = EmailMessage()
    message["From"] = smtp_user
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(
            smtp_host, smtp_port, timeout=30
        ) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)

        logging.info("SMTP accepted message for %s", recipient)
        print(f"SMTP ACCEPTED: {recipient}")
        return "SMTP_ACCEPTED"

    except (smtplib.SMTPException, OSError) as exc:
        logging.error(
            "SMTP failed for %s: %s", recipient, exc
        )
        print(f"FAILED: {recipient} - {exc}")
        return "FAILED"
