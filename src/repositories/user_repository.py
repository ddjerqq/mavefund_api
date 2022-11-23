from __future__ import annotations

import aiosqlite
from src.models.user import User
from src.repositories.repository_base import RepositoryBase


class UserRepository(RepositoryBase):
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self.__conn = connection
        self.__curs = cursor

    async def get_by_username(self, username: str) -> User | None:
        await self.__curs.execute("""
        SELECT *
        FROM "user"
        WHERE
            username = :username
        """, {"username": username})

        if (row := await self.__curs.fetchone()) is not None:
            return User.from_db(row)

    async def get_by_email(self, email):
        await self.__curs.execute("""
        SELECT *
        FROM "user"
        WHERE
            email = :email
        """, {"email": email})

        if (row := await self.__curs.fetchone()) is not None:
            return User.from_db(row)

    async def save_changes(self) -> None:
        await self.__conn.commit()

    async def get_all(self) -> list[User]:
        await self.__curs.execute("""
        SELECT *
        FROM "user"
        """)

        rows = await self.__curs.fetchall()
        return list(map(User.from_db, rows))

    async def get_by_id(self, id: int) -> User | None:
        await self.__curs.execute("""
        SELECT *
        FROM "user"
        WHERE
            id = :id
        """, {"id": id})

        if (row := await self.__curs.fetchone()) is not None:
            return User.from_db(row)

    async def add(self, entity: User) -> None:
        await self.__curs.execute("""
        INSERT INTO "user"
        (id, username, email, password_hash, rank)
        VALUES 
        (
            :id,
            :username,
            :email,
            :password_hash,
            :rank
        )
        """, entity.dict())

    async def update(self, entity: User) -> None:
        await self.__curs.execute("""
        UPDATE "user"
        SET
            username = :username,
            email = :email,
            password_hash = :password_hash,
            rank = :rank
        WHERE
            id = :id
        """, entity.dict())

    async def delete(self, id: int) -> None:
        await self.__curs.execute("""
        DELETE FROM "user"
        WHERE
            id = :id
        """, {"id": id})
