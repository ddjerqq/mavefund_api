import os

from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jose import jwt
from starlette.requests import Request

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


async def send_mail(subject: str, recipients: list, body) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="html"  # type: ignore
    )

    # Send the email
    fm = FastMail(MAIL_CONFIG)
    await fm.send_message(message)


async def send_verification_email(user: User) -> None:
    subject = "Verify your email address"

    html = render_template(
        "email/email.html",
        {
            "request": Request({"host": "127.0.0.1", "type": "http"}),
            "title": "Verify E-Mail",
            "description": "Please verify your E-Mail address",
            "subject": subject,
            "user": user.dict(),
            "url": f"{os.getenv('BASE_URL')}/api/v1/auth/verify-email/{user.verification_code}",
            "button_text": "verify email",
        }
    )

    await send_mail(subject, [user.email], html.body)


async def send_reset_password_email(user: User) -> None:
    subject = "Reset your password"

    expires = datetime.now() + timedelta(days=2)
    claims = {
        "sub": str(user.id),
        "exp": int(expires.timestamp()),
    }
    token = jwt.encode(claims, key=os.getenv("JWT_SECRET"))

    html = render_template(
        "email/email.html",
        {
            "request": Request({"host": "127.0.0.1", "type": "http"}),
            "title": "Reset password",
            "description": "Please reset your password",
            "subject": subject,
            "user": user.dict(),
            "url": f"{os.getenv('BASE_URL')}/reset.html?token={token}",
            "button_text": "verify email",
        }
    )

    await send_mail(subject, [user.email], html.body)
