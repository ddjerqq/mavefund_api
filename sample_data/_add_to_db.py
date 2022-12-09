import aiosqlite

from utilities.csv_parser import CsvDataParser
from repositories.record_repository import RecordRepository
import os
import asyncio as aio


paths = [
    file
    for file in os.listdir("")
    if file.endswith(".csv")
]

records = (
    record
    for records in map(CsvDataParser.parse, paths)
    for record in records
)


async def main():
    loop = aio.get_running_loop()
    conn = aiosqlite.connect("../app.db", loop=loop)
    conn = await conn.__aenter__()
    curs = await conn.cursor()

    repo = RecordRepository(conn, curs)
    futures = map(repo.add, records)

    await aio.gather(*futures)
    await repo.save_changes()
    # TODO rewrite to postgres


aio.run(main())
