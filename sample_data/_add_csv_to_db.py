import asyncio as aio
import aiofiles

import asyncpg
import os

from dotenv import load_dotenv


async def read_file(filepath: str) -> tuple[str, str]:
    *_, filename = filepath.split("/")
    symbol, *_ = filename.split(" ")
    async with aiofiles.open(filename) as f:
        content = await f.read()
    return symbol, content


async def main():
    load_dotenv()
    conn: asyncpg.Connection = await asyncpg.connect(
        host=os.getenv("HOST"),
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD"),
        database="mavefund",
    )

    symbol_filenames = await aio.gather(*[
        read_file(file)
        for file in os.listdir(".")
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


if __name__ == "__main__":
    aio.run(main())
