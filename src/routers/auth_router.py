from __future__ import annotations

from fastapi import APIRouter
from fastapi import Form
from fastapi import HTTPException

from src.data import ApplicationDbContext
from src.models.user import User
from src.models.dto import UserRegister, UserLogin
from src.utilities import Password


class AuthRouter:
    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(prefix="/auth")

        self.router.add_api_route("/register", self.register, methods=["POST"])
        self.router.add_api_route("/login", self.login, methods=["POST"])

    async def register(self, email: str = Form(), username: str = Form(), password: str = Form()) -> str:
        if await self.db.users.get_by_email(email):
            raise HTTPException(status_code=400, detail="email are already registered")

        if await self.db.users.get_by_username(username):
            raise HTTPException(status_code=400, detail="username are already registered")

        # TODO: change the rank depending on the payment later, we will also need to verify captcha and
        #  email address
        user = User.new(username, email, password, 0)
        await self.db.users.add(user)

        return user.jwt_token

    async def login(self, username: str = Form(), password: str = Form()) -> str:
        user = await self.db.users.get_by_username(username)

        if not user:
            raise HTTPException(status_code=404, detail="username not registered")

        if not Password.compare(user.password_hash, password):
            raise HTTPException(status_code=400, detail="password are incorrect")

        return user.jwt_token
