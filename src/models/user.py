from __future__ import annotations
from typing import Optional
import os
from datetime import datetime, timedelta

import asyncpg
from pydantic import BaseModel
from jose import jwt
from src.utilities import Password, Snowflake

ROLES = ["basic", "premium", "super", "admin"]


class User(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str
    rank: int
    verified: Optional[bool] = False
    """int: no sub = -1, basic user = 0, premium = 1, super_user = 2, admin = 3"""

    @classmethod
    def from_db(cls, row: asyncpg.Record) -> User:
        return cls(
            id=row["id"],
            username=row["username"],
            email=row["email"].strip(),
            password_hash=row["password_hash"],
            rank=row["rank"],
            verified=row["verified"]
        )

    @property
    def created_at(self) -> datetime:
        return Snowflake.created_at(self.id)

    @property
    def jwt_token(self) -> str:
        expires = datetime.now() + timedelta(minutes=60)
        claims = {
            "sub": str(self.id),
            "exp": int(expires.timestamp()),
        }
        return jwt.encode(claims, key=os.getenv("JWT_SECRET"))

    @property
    def api_key(self):
        expires = datetime.now() + timedelta(days=90)
        claims = {
            "sub": str(self.id),
            "exp": int(expires.timestamp()),
        }
        return jwt.encode(claims, key=os.getenv("JWT_SECRET"))

    @property
    def verification_code(self) -> str:
        expires = datetime.now() + timedelta(days=2)
        claims = {
            "sub": str(self.id),
            "exp": int(expires.timestamp()),
        }
        return jwt.encode(claims, key=os.getenv("JWT_SECRET"))

    @classmethod
    def new(cls, username: str, email: str, password: str, rank: int, verified: bool) -> User:
        return cls(
            id=Snowflake(),
            username=username,
            email=email,
            password_hash=Password.new(password),
            rank=rank,
            verified=verified
        )
