from __future__ import annotations

import os
from os.path import join

import aiofiles
import asyncpg
# TODO issue here vvvvvv
from src.services import UserService, CompanyInfoService
from src import PATH
# mavefund_api/


class ApplicationDbContext:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

        self.users = UserService(pool)
        self.companies = CompanyInfoService(pool)
        # TODO add migrations, which get executed on start


    async def migrate(self) -> None:
        files = sorted(
            file
            for file in os.listdir(join(PATH, ".migration"))
            if file.endswith(".sql")
        )

        async with self._pool.acquire() as conn:
            for file in files:
                async with aiofiles.open(join(PATH, ".migration", file)) as f:
                    content = await f.read()
                    await conn.execute(content)

    @classmethod
    async def connect(
            cls,
            host: str,
            user: str,
            password: str,
            database: str,
            *,
            port: int = 5432,
    ) -> ApplicationDbContext:
        # f"postgresql://{user}:{password}@{host}:{port}/{database}",
        pool = await asyncpg.create_pool(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
            min_size=10,
            max_size=100
        )
        return cls(pool)
