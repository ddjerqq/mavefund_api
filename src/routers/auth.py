from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException

from src.data import ApplicationDbContext
from src.models.user import User
from src.models.dto import UserRegister, UserLogin
from src.utilities import Password
from src.utilities import Snowflake


class AuthRouter:
    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(prefix="/auth")

        self.router.add_api_route("/register", self.register, methods=["POST"])
        self.router.add_api_route("/login", self.login, methods=["POST"])

    async def register(self, user_register: UserRegister) -> str:
        all_users = await self.db.users.get_all()
        if any(u.username == user_register.username or u.email == user_register.email for u in all_users):
            raise HTTPException(status_code=400, detail="username or email are already registered")

        user = User(
            id=Snowflake(),
            username=user_register.username,
            email=user_register.email,
            password_hash=Password.new(user_register.password),
            rank=0
        )

        await self.db.users.add(user)

        return user.jwt_token

    async def login(self, user_login: UserLogin) -> str:
        user = await self.db.users.get_by_username(user_login.username)
        if user and Password.compare(user.password_hash, user_login.password):
            return user.jwt_token
        else:
            raise HTTPException(status_code=400, detail="username or password are incorrect")
