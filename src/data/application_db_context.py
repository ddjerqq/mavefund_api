from __future__ import annotations

import asyncio as aio
import aiosqlite

from src.services import UserAuthService, UserService


class ApplicationDbContext:
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor) -> None:
        self.__connection = connection
        self.__cursor = cursor

        self.users = UserService(connection, cursor)
        self.auth  = UserAuthService(self)

    @classmethod
    async def connect(cls, db_path: str, *, loop: aio.AbstractEventLoop = None) -> ApplicationDbContext:
        connection = await aiosqlite.connect(db_path, loop=loop)
        cursor     = await connection.cursor()
        return cls(connection, cursor)
