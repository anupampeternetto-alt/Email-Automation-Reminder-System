
import aiosmtplib
from email.message import EmailMessage
from email.utils import formataddr

class Mailer:
    def __init__(self, host="smtp.gmail.com", port=465,
                 username=None, password=None, dry_run=True):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dry_run = dry_run

    async def send_html(self, from_name, from_email,
                        to_email, subject, html):
        msg = EmailMessage()
        msg["From"] = formataddr((from_name, from_email))
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content("Please view this email in HTML format.")
        msg.add_alternative(html, subtype="html")

        if self.dry_run:
            print("DRY RUN: Email simulated successfully")
            print("TO:", to_email)
            print("SUBJECT:", subject)
            return {"ok": True, "simulated": True}

        if not self.username or not self.password:
            return {"ok": False, "error": "SMTP credentials missing"}

        try:
            await aiosmtplib.send(
                msg,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=(self.port == 465),
                start_tls=(self.port == 587),
            )
            return {"ok": True, "simulated": False}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
