from __future__ import annotations

import logging
import os
import typing
from jose import JWTError, jwt

from src.models.user import User
if typing.TYPE_CHECKING:
    from src.data import ApplicationDbContext


class UserAuthService:
    def __init__(self, db: ApplicationDbContext) -> None:
        self.__users = db.users

    def extract_claims_from_jwt(self, token: str) -> dict[str, ...] | None:
        """Extract claims from JWT token

        returns the claims if the JWT is valid, None otherwise
        """
        try:
            return jwt.decode(
                token,
                os.getenv("JWT_SECRET"),
                algorithms=["HS256"]
            )
        except JWTError:
            logging.error("JWTError", exc_info=True)
            return None

    async def get_user_from_token(self, token: str) -> User | None:
        """Get user from token
        if this method returns None, raise 401 HTTPException
        """

        if (claims := self.extract_claims_from_jwt(token)) is None:
            return None

        user_id = int(claims.get("sub"))

        if user_id is None:
            return None

        return await self.__users.get_by_id(user_id)
