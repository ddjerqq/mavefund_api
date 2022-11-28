from __future__ import annotations

from fastapi import APIRouter
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

    async def register(self, user_register: UserRegister) -> str:
        if await self.db.users.get_by_email(user_register.email):
            raise HTTPException(status_code=400, detail="email are already registered")

        if await self.db.users.get_by_username(user_register.username):
            raise HTTPException(status_code=400, detail="username are already registered")

        user = User.new(user_register.username, user_register.email, user_register.password, user_register.rank)
        await self.db.users.add(user)

        return user.jwt_token

    async def login(self, user_login: UserLogin) -> str:
        user = await self.db.users.get_by_username(user_login.username)

        if not user:
            raise HTTPException(status_code=404, detail="username not registered")

        if not Password.compare(user.password_hash, user_login.password):
            raise HTTPException(status_code=400, detail="password are incorrect")

        return user.jwt_token
