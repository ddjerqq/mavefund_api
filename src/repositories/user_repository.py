from __future__ import annotations

import asyncpg
from src.models.user import User
from src.repositories.repository_base import RepositoryBase


class UserRepository(RepositoryBase):
    def __init__(self, connection: asyncpg.Connection):
        self.__conn = connection

    async def get_by_username(self, username: str) -> User | None:
        row = await self.__conn.fetchrow("""
        SELECT *
        FROM app_user
        WHERE
            username = $1
        """, username)

        if row is not None:
            return User.from_db(row)

    async def get_by_email(self, email):
        row = await self.__conn.fetchrow("""
        SELECT *
        FROM app_user
        WHERE
            email = $1
        """, email)

        if row is not None:
            return User.from_db(row)

    async def get_all(self) -> list[User]:
        rows = await self.__conn.fetch("""
        SELECT *
        FROM app_user
        """)

        return list(map(User.from_db, rows))

    async def get_by_id(self, id: int) -> User | None:
        row = await self.__conn.fetchrow("""
        SELECT *
        FROM app_user
        WHERE
            id = $1
        """, id)

        if row is not None:
            return User.from_db(row)

    async def add(self, entity: User) -> None:
        await self.__conn.execute("""
        INSERT INTO app_user
        (id, username, email, password_hash, rank)
        VALUES 
        (
            $1,
            $2,
            $3,
            $4,
            $5
        )
        """, *entity.dict().values())

    async def update(self, entity: User) -> None:
        await self.__conn.execute("""
        UPDATE app_user
        SET
            username = $2,
            email = $3,
            password_hash = $4,
            rank = $5
        WHERE
            id = $1
        """, *entity.dict().values())

    async def delete(self, id: int) -> None:
        await self.__conn.execute("""
        DELETE FROM app_user
        WHERE
            id = $1
        """, id)
