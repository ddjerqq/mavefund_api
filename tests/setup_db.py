import asyncio as aio
import os

import asyncpg

print(os.getcwd())
print(os.listdir(os.getcwd()))
with open("../sql/0-create-model-user.sql") as user, open("../sql/0-create-model-record.sql") as record:
    user = user.read()
    record = record.read()


async def main():
    async with asyncpg.connect(
            user='postgres',
            password='password',
            database='postgres',
            host='localhost'
    ) as conn:
        await conn.execute(user)
        await conn.execute(record)


if __name__ == "__main__":
    aio.run(main())
