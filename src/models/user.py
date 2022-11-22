from __future__ import annotations

import os
from datetime import datetime, timedelta

import aiosqlite
from pydantic import BaseModel
from jose import jwt

from src.utilities.password_hasher import Password
from src.utilities.snowflake import Snowflake


class User(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str
    rank: int
    # TODO add discord-like permissions
    #  bit shifted values,
    #  0 = no permissions,
    #  1 = read,
    #  2 = write,
    #  4 = admin,
    #  8 = owner
    # so on

    @classmethod
    def from_db(cls, row: aiosqlite.Row) -> User:
        return cls(
            id=row[0],
            username=row[1],
            email=row[2],
            password_hash=row[3],
            rank=row[4],
        )

    @property
    def created_at(self) -> datetime:
        return Snowflake.created_at(self.id)

    @property
    def jwt_token(self) -> str:
        expires = datetime.utcnow() + timedelta(minutes=60)
        claims = {
            "sub": self.id,
            "exp": int(expires.timestamp()),
        }
        return jwt.encode(claims, key=os.getenv("JWT_SECRET"))

    @classmethod
    def new(cls, username: str, email: str, password: str) -> User:
        return cls(
            id=Snowflake(),
            username=username,
            email=email,
            password=Password.new(password),
        )
