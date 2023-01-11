from __future__ import annotations

import logging.config
import os
from os.path import dirname, realpath, join
import asyncio as aio

import asyncpg
import aiofiles


logging.config.fileConfig("logging.conf")
log = logging.getLogger("setup")

# mavefund_api/
PATH = dirname(realpath(__file__))


files = sorted(
    (
        join(PATH, "sql", file)
        for file in os.listdir("sql")
        if file.endswith(".sql")
    ),
    # potential issue for double-digit migrations,
    # thought i doubt we would ever reach that level, so for now it's okay
    key=lambda filename: next(map(int, filter(str.isdigit, filename)))
)


conn: asyncpg.Connection | None = None


async def init():
    global conn
    log.info("migration initializing")
    conn = await asyncpg.connect(
        host=os.getenv("HOST"),
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")
    )
    log.info("migration initialized")


async def up():
    log.info("migration UP started")
    for file in files:
        async with aiofiles.open(file) as f:
            content = await f.read()
            await conn.execute(content)
    log.info("migration UP finished successfully")


async def down():
    log.info("migration DOWN started")
    await conn.execute("""
    DROP TABLE app_user;
    DROP TABLE stock_record;
    DROP TABLE csv_data;
    """)
    log.info("migration DOWN finished successfully")


async def main():
    os.environ["HOST"] = "31.220.57.57"
    await init()
    await up()


if __name__ == "__main__":
    aio.run(main())
