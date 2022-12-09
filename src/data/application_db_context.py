from __future__ import annotations

import asyncio as aio
import asyncpg

from src.services import UserService, RecordService


class ApplicationDbContext:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.__connection = pool

        self.users = UserService(pool)
        self.records = RecordService(pool)

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
        # f"postgresql://{user}:{password}@{host}:{port}/{database}",
        pool = await asyncpg.create_pool(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,

            min_size=10,
            max_size=30,
            loop=loop
        )
        return cls(pool)
