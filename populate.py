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
        content = content.strip("﻿")
    info = await CsvDataParser.parse(filepath)
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


async def down():
    log.info("starting tearing DOWN the data")
    await conn.execute("""
    DELETE FROM stock_record;
    DELETE FROM app_user;
    DELETE FROM csv_data;
    """)
    log.info("tearing DOWN data done")



async def main():
    os.environ["POSTGRES_HOST"] = "127.0.0.1"
    await init()
    await up()


if __name__ == "__main__":
    aio.run(main())
