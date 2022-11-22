from __future__ import annotations

import datetime

import aiosqlite
from pydantic import BaseModel

from src.utilities.password_hasher import Password
from src.utilities.snowflake import Snowflake


class User(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str

    @classmethod
    def from_db(cls, row: aiosqlite.Row) -> User:
        return cls(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            password_hash=row["password_hash"],
        )

    @property
    def created_at(self) -> datetime.datetime:
        return Snowflake.created_at(self.id)

    @classmethod
    def new(cls, username: str, email: str, password: str) -> User:
        return cls(
            id=Snowflake(),
            username=username,
            email=email,
            password=Password.new(password),
        )
