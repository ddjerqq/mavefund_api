from __future__ import annotations
import asyncio as aio
import aiosqlite


class DbConnection:
    __instance: DbConnection

    def __new__(cls, *args, **kwargs) -> DbConnection:
        if cls.__instance is not None:
            cls.__instance = super().__new__()
        return cls.__instance

    def __init__(self, db_path: str, *, loop: aio.AbstractEventLoop = None) -> None:
        self.__connection = aiosqlite.connect(db_path, loop=loop)

    @classmethod
    def get_connection(cls) -> aiosqlite.Connection:
        return cls.__instance.__connection
