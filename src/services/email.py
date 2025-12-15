import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_email(to: str, subject: str, content: str):
    msg = EmailMessage()
    msg["From"] = settings.SMTP_FROM_EMAIL
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(content)

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        if settings.SMTP_TLS:
            server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
