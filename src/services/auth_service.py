from __future__ import annotations

import os

import aiosqlite

from jose import JWTError, jwt

from src.models.user import User
from src.services import UserService
from src.utilities import Password


class UserAuthService:
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor) -> None:
        self.__users = UserService(connection, cursor)

    async def authenticate(self, username: str, password: str) -> User | None:
        user = await self.__users.get_by_username(username)

        if user and Password.compare(user.password_hash, password):
            return user

        return None

    async def get_user_from_token(self, token: str) -> User | None:
        """Get user from token
        if this method returns None, raise 401 HTTPException
        """

        # credentials_exception = HTTPException(
        #     status_code=401,
        #     detail="Could not validate credentials",
        # )

        try:
            claims = jwt.decode(token, os.getenv("JWT_SECRET"))
            user_id: int = claims.get("sub")

            if user_id is None:
                return None

        except JWTError:
            return None

        user = await self.__users.get_by_id(user_id)
        return user
