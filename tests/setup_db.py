import asyncio as aio
import os
import asyncpg


PATH = os.path.join(os.getcwd(), "sql")

with (
    open(os.path.join(PATH, "0-create-model-user.sql")) as user,
    open(os.path.join(PATH, "0-create-model-record.sql")) as record,
):
    user_query = user.read()
    record_query = record.read()


async def main():
    async with asyncpg.connect(
            user='postgres',
            password='password',
            database='postgres',
            host='localhost'
    ) as conn:
        await conn.execute(user_query)
        await conn.execute(record_query)


if __name__ == "__main__":
    aio.run(main())
