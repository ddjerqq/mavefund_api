from __future__ import annotations

import asyncpg
from src.models.user import User
from src.repositories.repository_base import RepositoryBase


class UserRepository(RepositoryBase):
    def __init__(self, pool: asyncpg.Pool):
        self.__pool = pool

    async def get_by_username(self, username: str) -> User | None:
        async with self.__pool.acquire(timeout=60) as conn:
            row = await conn.fetchrow("""
            SELECT *
            FROM app_user
            WHERE
                username = $1
            """, username)

            if row is not None:
                return User.from_db(row)

    async def get_by_email(self, email):
        async with self.__pool.acquire(timeout=60) as conn:
            row = await conn.fetchrow("""
                SELECT *
                FROM app_user
                WHERE
                    email = $1
                """, email)

            if row is not None:
                return User.from_db(row)

    async def get_all(self) -> list[User]:
        async with self.__pool.acquire(timeout=60) as conn:
            rows = await conn.fetch("""
        SELECT *
        FROM app_user
            """)

            return list(map(User.from_db, rows))

    async def get_by_id(self, id: int) -> User | None:
        async with self.__pool.acquire(timeout=60) as conn:
            row = await conn.fetchrow("""
            SELECT *
            FROM app_user
            WHERE
                id = $1
            """, id)

            if row is not None:
                return User.from_db(row)

    async def add(self, entity: User) -> None:
        async with self.__pool.acquire(timeout=60) as conn:
            await conn.execute("""
        INSERT INTO app_user
        (id, username, email, password_hash, rank,verified)
        VALUES 
        (
            $1,
            $2,
            $3,
            $4,
            $5,
            $6
        )
        """, *entity.dict().values())

    async def update(self, entity: User) -> None:
        async with self.__pool.acquire(timeout=60) as conn:
            await conn.execute("""
        UPDATE app_user
        SET
            username = $2,
            email = $3,
            password_hash = $4,
            rank = $5,
            verified = $6
        WHERE
            id = $1
        """, *entity.dict().values())

    async def delete(self, id: int) -> None:
        async with self.__pool.acquire(timeout=60) as conn:
            await conn.execute("""
        DELETE FROM app_user
        WHERE
            id = $1
        """, id)
