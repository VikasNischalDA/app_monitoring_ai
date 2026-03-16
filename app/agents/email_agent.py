import smtplib
from email.mime.text import MIMEText
import os

class EmailAgent:

    def send_email(self, body: str):
        msg = MIMEText(body)
        msg["Subject"] = "Application Health Alert"
        msg["From"] = os.getenv("EMAIL_FROM")
        msg["To"] = os.getenv("EMAIL_TO")

        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)