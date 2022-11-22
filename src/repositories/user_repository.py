from __future__ import annotations

import aiosqlite
from fastapi import Depends

from src.models.user import User
from src.dependencies.database_connection import DbConnection
from src.repositories.repository_base import RepositoryBase


class UserRepository(RepositoryBase):
    def __init__(self, db_conn_pool: DbConnection = Depends()):
        self.__conn = db_conn_pool.get_connection()

    async def save_changes(self) -> None:
        await self.__conn.commit()

    async def get_all(self) -> list[User]:
        cursor: aiosqlite.Cursor = await self.__conn.cursor()

        await cursor.execute("""
        SELECT *
        FROM "user"
        """)

        rows = await cursor.fetchall()
        return list(map(User.from_db, rows))

    async def get_by_id(self, id: int) -> User | None:
        cursor: aiosqlite.Cursor = await self.__conn.cursor()

        await cursor.execute("""
        SELECT *
        FROM "user"
        WHERE
            id = :id
        """, {"id": id})

        row = await cursor.fetchone()
        return User.from_db(row)

    async def add(self, entity: User) -> None:
        cursor: aiosqlite.Cursor = await self.__conn.cursor()

        await cursor.execute("""
        INSERT INTO "user"
        VALUES 
        (
            id = :id,
            username = :username,
            email = :email,
            password_hash = :password_hash,
            rank = :rank
        )
        """, entity.dict())

    async def update(self, entity: User) -> None:
        cursor: aiosqlite.Cursor = await self.__conn.cursor()

        await cursor.execute("""
        UPDATE "user"
        SET
            username = :username,
            email = :email,
            password_hash = :password_hash,
            rank = :rank
        WHERE
            id = :id
        """, entity.dict())

    async def delete(self, entity: User) -> None:
        cursor: aiosqlite.Cursor = await self.__conn.cursor()

        await cursor.execute("""
        DELETE FROM "user"
        WHERE
            id = :id
        """, {"id": entity.id})
