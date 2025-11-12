import smtplib
from email.mime.text import MIMEText
from dotenv import  load_dotenv
import os
load_dotenv()

def send_email(to_email: str, subject: str, body: str):
    sender_email:str = os.getenv("SENDER_EMAIL")
    sender_password:str = os.getenv("SENDER_PASSWORD")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("✅ Email sent successfully")
    except Exception as e:
        print(f"❌ Email send failed: {e}")
