from __future__ import annotations

import logging.config
import os
from os.path import dirname, realpath, join
import asyncpg
import asyncio as aio
import aiofiles

from src.utilities.csv_parser import CsvDataParser
from src.models import User

# mavefund_api/
PATH = dirname(realpath(__file__))


logging.config.fileConfig(join(PATH, "logging.conf"))
log = logging.getLogger("setup")



files = [
    join(PATH, "sample_data", file)
    for file in os.listdir(join(PATH, "sample_data"))
    if file.endswith(".csv")
]

records = (
    record
    for file in files
    for record in CsvDataParser.parse(file)
)


conn: asyncpg.Connection | None = None


async def init():
    global conn
    log.info("populate initializing")
    conn = await asyncpg.connect(
        host=os.getenv("HOST"),
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")
    )
    log.info("populate initialized")


async def _record_up():
    log.info("records going UP")
    record_payload = (
        tuple(record.flat_dict().values())
        for record in records
    )

    try:
        await conn.executemany("""
        INSERT INTO stock_record
        VALUES
        (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, 
            $24, $25, $26, $27, $28, $29, $30, $31, $32, $33, $34, $35, $36, $37, $38, $39, $40, $41, $42, $43, $44, 
            $45, $46, $47, $48, $49, $50, $51, $52, $53, $54, $55, $56, $57, $58, $59, $60, $61, $62, $63, $64, $65, 
            $66, $67, $68, $69, $70, $71, $72, $73, $74, $75, $76, $77, $78, $79, $80, $81, $82, $83, $84, $85, $86, 
            $87, $88, $89
        )
        """, record_payload)
    except:
        log.exception(
            "error occurred while inserting records inside the database",
            exc_info=True
        )
    else:
        log.info("records are UP")


async def _test_users_up():
    # password is "password"
    log.info("test users going UP")
    pw = "$2b$08$Fr4c.uB6ZlVzH8kXJ8Kmyu0G0RjobQtZ1slNMbWXI5NEJdMVgE2zq"
    users = [
        User(id=1001, username="free", email="free@mavefund.com", password_hash=pw, rank=-1, verified=True),
        User(id=1002, username="basic", email="basic@mavefund.com", password_hash=pw, rank=0, verified=True),
        User(id=1003, username="premium", email="premium@mavefund.com", password_hash=pw, rank=1, verified=True),
        User(id=1004, username="super", email="super@mavefund.com", password_hash=pw, rank=2, verified=True),
        User(id=1005, username="admin", email="admin@mavefund.com", password_hash=pw, rank=3, verified=True),
    ]

    try:
        await conn.execute("""
            INSERT INTO app_user
            (id, username, email, password_hash, rank, verified)
            VALUES 
            (
                $1,
                $2,
                $3,
                $4,
                $5,
                $6
            )
            """, map(lambda user: user.dict().values(), users))
    except:
        log.exception(
            "error occurred while inserting test users inside the database",
            exc_info=True
        )
    else:
        log.info("test users are UP")


async def _read_file(filepath: str) -> tuple[str, str]:
    _, tail = os.path.split(filepath)
    symbol, *_ = tail.split(" ")
    async with aiofiles.open(filepath) as f:
        content = await f.read()
    return symbol, content


async def _csv_data_up():
    log.info("csv files going UP")
    symbol_filenames = await aio.gather(*[
        _read_file(join(PATH, "sample_data", file))
        for file in os.listdir("sample_data")
        if file.endswith(".csv")
    ])

    await conn.executemany("""
    INSERT INTO csv_data
    VALUES 
    (
        $1,
        $2
    )
    """, symbol_filenames)
    log.info("csv files are UP")


async def up():
    log.info("starting populating the database")
    await _record_up()
    # await _test_users_up()
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
    await init()
    await up()


if __name__ == "__main__":
    aio.run(main())
