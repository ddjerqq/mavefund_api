from __future__ import annotations

import asyncio as aio
import asyncpg

from src.services import UserService, RecordService


class ApplicationDbContext:
    def __init__(self, connection: asyncpg.Connection) -> None:
        self.__connection = connection

        self.users = UserService(connection)
        self.records = RecordService(connection)

    @classmethod
    async def connect(
            cls,
            host: str,
            user: str,
            password: str,
            database: str,
            *,
            port: int = 5432,
            loop: aio.AbstractEventLoop = None
    ) -> ApplicationDbContext:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            loop=loop or aio.get_event_loop()
        )
        return cls(conn)
