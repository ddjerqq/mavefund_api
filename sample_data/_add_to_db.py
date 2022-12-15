import asyncpg
from rgbprint import rgbprint

from utilities.csv_parser import CsvDataParser
from repositories.record_repository import RecordRepository
import os
import asyncio as aio


records = (
    record
    for file in os.listdir(".")
    if file.endswith(".csv")
    for record in CsvDataParser.parse(file)
)


async def main():
    pool = await asyncpg.create_pool(
        host=os.getenv("HOST"),
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD"),
        database="mavefund",
        loop=aio.get_running_loop()
    )

    repo = RecordRepository(pool)

    for record in records:
        rgbprint(f">>> adding record with id: {record.id}", color="green")
        try:
            await repo.add(record)
        except Exception as e:
            rgbprint(f"error: {e}", color="red")
        rgbprint(f"<<< added record with id:  {record.id}", color="green")


aio.run(main())
