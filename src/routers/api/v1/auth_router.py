from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse

from src.data import ApplicationDbContext
from src.models.user import User
from src.models.dto import UserRegister, UserLogin, ResetPassword, ResetPasswordVerify
from src.utilities import Password, extract_claims_from_jwt
from src.dependencies.auth import subscriber_only
from src.dependencies.validate_captcha_token import validate_captcha_token
from src.utilities.email_utilities import send_verification_email, send_reset_password_email


class AuthRouter:
    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(prefix="/auth")

        self.router.add_api_route(
            "/register",
            self.register,
            methods=["POST"],
            dependencies=[Depends(validate_captcha_token)],
        )

        self.router.add_api_route(
            "/login",
            self.login,
            methods=["POST"],
            dependencies=[Depends(validate_captcha_token)],
        )

        self.router.add_api_route(
            "/api-key",
            self.api_key,
            methods=["GET"],
            dependencies=[Depends(subscriber_only)],
            response_model=str
        )

        self.router.add_api_route(
            "/verify-email/{token:str}",
            self.verify_email,
            methods=["GET"]
        )

        self.router.add_api_route(
            "/reset-password",
            self.reset_password,
            methods=["POST"]
        )

        self.router.add_api_route(
            "/reset-password-verify/{token:str}",
            self.reset_password_verify,
            methods=["POST"]
        )

    async def register(self, register: UserRegister):
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

        await send_verification_email(user)

        return {"message": "please verify your email address. check your email inbox"}

    async def login(self, login: UserLogin) -> str:
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

    async def verify_email(self, token: str):
        claims = extract_claims_from_jwt(token)
        if claims is None:
            raise HTTPException(status_code=400, detail="Invalid Token!")

        id = claims["sub"]
        id = int(id)
        user = await self.db.users.get_by_id(id)

        user.verified = True

        await self.db.users.update(user)

        return RedirectResponse(url="/login", status_code=302)

    async def reset_password(self, reset: ResetPassword):
        user = await self.db.users.get_by_email(reset.email)

        if user is None:
            raise HTTPException(status_code=400, detail="There is no account with this email!")

        await send_reset_password_email(user, reset.new_password)

        return RedirectResponse(url="/login", status_code=302)

    async def reset_password_verify(self, token: str) -> str:
        claims = extract_claims_from_jwt(token)
        if claims is None:
            raise HTTPException(status_code=400, detail="Invalid Token!")

        id = claims["sub"]
        id = int(id)
        user = await self.db.users.get_by_id(id)

        new_password = claims["np"]

        if not user:
            raise HTTPException(status_code=400, detail="user is not found")

        user.verified = True
        user.password_hash = Password.new(new_password)
        await self.db.users.update(user)

        return user.jwt_token
