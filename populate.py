from __future__ import annotations

import logging.config
import os
from os.path import dirname, realpath, join
import asyncpg
import asyncio as aio
import aiofiles

from src.utilities.csv_parser import CsvDataParser

# mavefund_api/
PATH = dirname(realpath(__file__))


logging.config.fileConfig(join(PATH, "logging.conf"))
log = logging.getLogger("setup")


files = [
    join(PATH, "sample_data", file)
    for file in os.listdir(join(PATH, "sample_data"))
    if file.endswith(".csv")
]


conn: asyncpg.Connection | None = None


async def init():
    global conn
    log.info("populate initializing")
    conn = await asyncpg.connect(
        host=os.getenv("POSTGRES_HOST"),
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")
    )
    log.info("populate initialized")



async def _read_file(filepath: str) -> tuple[str, str, str]:
    async with aiofiles.open(filepath, encoding="utf-8") as f:
        content = await f.read()
        content = content.replace("﻿", "")
    info = await CsvDataParser.parse(path=filepath)
    return info.ticker, info.company_name, content


async def _csv_data_up():
    log.info("csv files going UP")
    symbol_filenames = await aio.gather(*[
        _read_file(join(PATH, "sample_data", file))
        for file in os.listdir("sample_data")
        if file.endswith(".csv")
    ])

    try:
        await conn.executemany("""
        INSERT INTO csv_data
        VALUES 
        (
            $1,
            $2,
            $3
        )
        ON CONFLICT DO NOTHING;
        """, symbol_filenames)
    except Exception as e:
        _ = e
        log.exception("error occurred while trying to insert csv data into the database", exc_info=True)
    log.info("csv files are UP")


async def up():
    log.info("starting populating the database")
    await _csv_data_up()
    log.info("populating the database finished successfully")

# password is "password"
# pw = "$2b$08$Fr4c.uB6ZlVzH8kXJ8Kmyu0G0RjobQtZ1slNMbWXI5NEJdMVgE2zq"
# users = [
#     User(id=1001, username="free", email="free@mavefund.com", password_hash=pw, rank=-1, verified=True),
#     1001,free,free@mavefund.com,$2b$08$Fr4c.uB6ZlVzH8kXJ8Kmyu0G0RjobQtZ1slNMbWXI5NEJdMVgE2zq,-1,true
#
#     User(id=1002, username="basic", email="basic@mavefund.com", password_hash=pw, rank=0, verified=True),
#     1002,basic,basic@mavefund.com,$2b$08$Fr4c.uB6ZlVzH8kXJ8Kmyu0G0RjobQtZ1slNMbWXI5NEJdMVgE2zq,0,true
#
#     User(id=1003, username="premium", email="premium@mavefund.com", password_hash=pw, rank=1, verified=True),
#     1003,premium,premium@mavefund.com,$2b$08$Fr4c.uB6ZlVzH8kXJ8Kmyu0G0RjobQtZ1slNMbWXI5NEJdMVgE2zq,1,true
#
#     User(id=1004, username="super", email="super@mavefund.com", password_hash=pw, rank=2, verified=True),
#     1004,super,super@mavefund.com,$2b$08$Fr4c.uB6ZlVzH8kXJ8Kmyu0G0RjobQtZ1slNMbWXI5NEJdMVgE2zq,2,true
#
#     User(id=1005, username="admin", email="admin@mavefund.com", password_hash=pw, rank=3, verified=True),
#     1005,admin,admin@mavefund.com,$2b$08$Fr4c.uB6ZlVzH8kXJ8Kmyu0G0RjobQtZ1slNMbWXI5NEJdMVgE2zq,3,true
# ]


async def main():
    # docker-compose
    # host = os.environ["POSTGRES_HOST"]

    # VPS host
    # host = os.getenv("HOST")

    # local host
    # host = "127.0.0.1"

    # uncomment if the target of data population is not the default database
    # os.environ["POSTGRES_HOST"] = host

    await init()
    await up()
    await conn.close()


if __name__ == "__main__":
    aio.run(main())
