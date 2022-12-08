from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..data import ApplicationDbContext
from ..models.user import User
from ..models.dto import UserRegister, UserLogin
from ..utilities import Password


class AuthRouter:
    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(prefix="/auth")

        self.router.add_api_route("/register", self.register, methods=["POST"])
        self.router.add_api_route("/login", self.login, methods=["POST"])

    async def register(self, register: UserRegister) -> str:
        if await self.db.users.get_by_email(register.email):
            raise HTTPException(status_code=409, detail="email is already registered")

        if await self.db.users.get_by_username(register.username):
            raise HTTPException(status_code=409, detail="username is already registered")

        # TODO: change the rank depending on the payment later, we will also need to verify captcha and
        #  email address
        user = User.new(register.username.lower(), register.email.lower(), register.password, 0)
        await self.db.users.add(user)

        return user.jwt_token

    async def login(self, login: UserLogin) -> str:
        user = await self.db.users.get_by_username(login.username)

        if not user:
            raise HTTPException(status_code=404, detail="username not registered")

        if not Password.compare(user.password_hash, login.password):
            raise HTTPException(status_code=400, detail="password is incorrect")

        return user.jwt_token
