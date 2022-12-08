import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("opening sql files")
    with open("0-create-model-user.sql", "r") as f:
        create_user = f.read()

    with open("0-create-model-record.sql", "r") as f:
        create_record = f.read()
    print("opening sql files done")

    async with asyncpg.connect(
        "postgres",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database="mavefund",
    ) as conn:
        print("creating tables")
        await conn.execute(create_user)
        await conn.execute(create_record)
        print("creating tables done")

    print("done")