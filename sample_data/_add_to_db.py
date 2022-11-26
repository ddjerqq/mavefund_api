import aiosqlite

from src.utilities.csv_parser import CsvDataParser
from src.repositories.record_repository import RecordRepository
import os
import asyncio as aio

paths = [
    file
    for file in os.listdir()
    if not file.startswith("_")
]

recordss = map(CsvDataParser.parse, filter(lambda f: "_" not in f, os.listdir()))


async def main():
    loop = aio.get_running_loop()
    conn = aiosqlite.connect("../app.db", loop=loop)
    conn = await conn.__aenter__()
    curs = await conn.cursor()

    repo = RecordRepository(conn, curs)

    futures = [
        repo.add(record)
        for records in recordss
        for record in records
    ]

    await aio.gather(*futures)

    await repo.save_changes()


aio.run(main())
