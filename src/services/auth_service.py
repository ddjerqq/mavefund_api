from __future__ import annotations

import logging
import os
import typing
from jose import JWTError, jwt

from dependencies import extract_claims_from_jwt
from src.models.user import User
if typing.TYPE_CHECKING:
    from src.data import ApplicationDbContext


class UserAuthService:
    def __init__(self, db: ApplicationDbContext) -> None:
        self.__users = db.users

    async def get_user_from_token(self, token: str) -> User | None:
        """Get user from token
        if this method returns None, raise 401 HTTPException
        """

        if (claims := extract_claims_from_jwt(token)) is None:
            return None

        user_id = int(claims.get("sub"))

        if user_id is None:
            return None

        return await self.__users.get_by_id(user_id)
