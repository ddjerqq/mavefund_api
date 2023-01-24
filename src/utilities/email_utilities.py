import os

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from src.models import User
from src.utilities.render_template import render_template


MAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASSWORD"),
    MAIL_FROM_NAME="Verify Email",
    MAIL_FROM=os.getenv("EMAIL_FROM"),  # type: ignore
    MAIL_PORT=os.getenv("EMAIL_PORT"),  # type: ignore
    MAIL_SERVER=os.getenv("EMAIL_HOST"),
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_mail(subject: str, recipients: list, body):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="html"  # type: ignore
    )

    # Send the email
    fm = FastMail(MAIL_CONFIG)
    await fm.send_message(message)


async def send_verification_email(user: User):
    subject = "Verify your email address"

    html = render_template(
        "email/email.html",
        {
            "title": "Verify E-Mail",
            "description": "Please verify your E-Mail address",
            "subject": subject,
            "user": user,
            "url": f"{os.getenv('BASE_URL')}/verify-email/{user.verification_code}",
            "button_text": "verify email",
        }
    )

    await send_mail(subject, [user.email], html)


async def send_reset_password_email(user: User):
    subject = "Reset your password"

    html = render_template(
        "email/email.html",
        {
            "title": "Reset password",
            "description": "Please reset your password",
            "subject": subject,
            "user": user,
            "url": f"{os.getenv('BASE_URL')}/reset-password-verify/{user.verification_code}",
            "button_text": "verify email",
        }
    )

    await send_mail(subject, [user.email], html)
