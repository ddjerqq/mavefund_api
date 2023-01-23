from __future__ import annotations

import os

import aiohttp
import requests
from fastapi import APIRouter, HTTPException, Request, Depends, BackgroundTasks

from src.data import ApplicationDbContext
from src.models.user import User
from src.models.dto import UserRegister, UserLogin, ResetPassword, ResetPasswordVerify
from src.utilities import Password, tokenizer
from src.dependencies.auth import subscriber_only
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.utilities.render_template import TEMPLATES

mail_conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('EMAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('EMAIL_PASSWORD'),
    MAIL_FROM_NAME="Verify Email",
    MAIL_FROM=os.getenv('EMAIL_FROM'),  # type: ignore
    MAIL_PORT=os.getenv('EMAIL_PORT'),  # type: ignore
    MAIL_SERVER=os.getenv('EMAIL_HOST'),
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


class AuthRouter:
    _recaptcha_secret_key = os.getenv("RECAPTCHA_SECRET")

    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(prefix="/auth")

        self.router.add_api_route(
            "/register",
            self.register,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/reset-password-verify",
            self.reset_password_verify,
            methods=["POST"]
        )

        self.router.add_api_route(
            "/login",
            self.login,
            methods=["POST"]
        )

        self.router.add_api_route(
            "/reset-password",
            self.reset_password,
            methods=["POST"]
        )

        self.router.add_api_route(
            "/api-key",
            self.api_key,
            methods=["GET"],
            dependencies=[Depends(subscriber_only)],
            response_model=str
        )

    async def register(self, register: UserRegister, request: Request, background_tasks: BackgroundTasks) -> str:
        await self._is_valid_recaptcha_token(register.recaptcha_token, request)

        if await self.db.users.get_by_email(register.email):
            raise HTTPException(status_code=409, detail="email is already registered")

        if await self.db.users.get_by_username(register.username):
            raise HTTPException(status_code=409, detail="username is already registered")

        user = User.new(
            register.username.lower(),
            register.email.lower(),
            register.password,
            -1,
            False
        )

        await self.db.users.add(user)

        token = tokenizer.encode_token(user.email)
        background_tasks.add_task(self.send_verification_mail, user, token)

        return "please verify your email address. check your email inbox"

    async def login(self, login: UserLogin, request: Request) -> str:
        await self._is_valid_recaptcha_token(login.recaptcha_token, request)
        user = await self.db.users.get_by_username(login.username)

        if not user:
            raise HTTPException(status_code=404, detail="username not registered")

        if not user.verified:
            raise HTTPException(status_code=400, detail="unverified")

        if not Password.compare(user.password_hash, login.password):
            raise HTTPException(status_code=400, detail="password is incorrect")

        return user.jwt_token

    async def api_key(self, req: Request) -> User:
        return req.user.api_key

    async def _is_valid_recaptcha_token(self, token: str, request: Request):
        recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {
            "secret": self._recaptcha_secret_key,
            "response": token,
            "remoteip": request.client.host,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(recaptcha_url, data=payload) as resp:
                result = await resp.json()

        if not result.get("success", False):
            raise HTTPException(status_code=400, detail="Invalid recaptcha!")

        return True

    async def reset_password(self, reset: ResetPassword, background_tasks: BackgroundTasks) -> str:
        user = await self.db.users.get_by_email(reset.email)
        if user is None:
            raise HTTPException(status_code=400, detail="There is no account with this email!")

        token = tokenizer.encode_token(user.email)
        background_tasks.add_task(self.send_password_reset_link, user, token)

        return "Reset password link has been sent to you, Please check your inbox!"

    async def reset_password_verify(self, form: ResetPasswordVerify) -> str:
        email = tokenizer.decode_token(form.token)

        if not email:
            raise HTTPException(status_code=400, detail="Invalid Token!")

        user = await self.db.users.get_by_email(email)
        if not email:
            raise HTTPException(status_code=400, detail="Not found")

        user.verified = True
        user.password_hash = Password.new(form.password)
        await self.db.users.update(user)

        return user.jwt_token

    async def _send_mail(self, subject: str, recipients: list, body):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype="html"  # type: ignore
        )

        # Send the email
        fm = FastMail(mail_conf)
        await fm.send_message(message)

    async def send_verification_mail(self, user: User, token: str):
        subject = "Verify your email address"
        template = TEMPLATES.get_template("verify/email.html")
        html = template.render(
            subject=subject,
            username=user.username,
            url=f"https://mavefund.com/verify-email/{token}"
        )
        await self._send_mail(subject, [user.email], html)

    async def send_password_reset_link(self, user: User, token: str):
        subject = "Password Reset"
        template = TEMPLATES.get_template('verify/password-reset.html')
        html = template.render(
            subject=subject,
            username=user.username,
            url=f"https://mavefund.com/reset-password-verify/{token}"
        )
        await self._send_mail(subject, [user.email], html)
