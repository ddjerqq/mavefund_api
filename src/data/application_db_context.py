from __future__ import annotations

import asyncio as aio
import aiosqlite

from ..services import UserAuthService, UserService, RecordService


class ApplicationDbContext:
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor) -> None:
        self.__connection = connection
        self.__cursor = cursor

        self.users = UserService(connection, cursor)
        self.records = RecordService(connection, cursor)
        self.auth = UserAuthService(self)

    @classmethod
    async def connect(cls, db_path: str, *, loop: aio.AbstractEventLoop = None) -> ApplicationDbContext:
        conn = await aiosqlite.connect(db_path, loop=loop or aio.get_running_loop())
        cursor = await conn.cursor()
        return cls(conn, cursor)
