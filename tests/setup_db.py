import asyncio as aio
import os
from os.path import join, realpath, dirname
import asyncpg


PATH = join(dirname(dirname(realpath(__file__))), "sql")

with (
    open(os.path.join(PATH, "0-create-model-user.sql")) as user,
    open(os.path.join(PATH, "0-create-model-record.sql")) as record,
):
    user_query = user.read()
    record_query = record.read()


async def main():
    conn = await asyncpg.connect(user='postgres', password='password', database='postgres', host='postgres')
    await conn.execute(user_query)
    await conn.execute(record_query)
    print("created test tables!")


if __name__ == "__main__":
    aio.run(main())
