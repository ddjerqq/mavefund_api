from __future__ import annotations

import asyncpg

from src.models import Record
from src.repositories.record_repository import RecordRepository
from src.services.service_base import ServiceBase


class RecordService(ServiceBase):
    def __init__(self, pool: asyncpg.Pool):
        self.__records = RecordRepository(pool)

    async def get_csv_by_symbol(self, symbol: str) -> str | None:
        return await self.__records.get_csv_by_symbol(symbol)

    async def get_all_by_company_name(self, name: str) -> dict:
        return await self.__records.get_all_by_company_name(name)

    async def get_all_by_symbol(self, username: str) -> list[Record]:
        return await self.__records.get_all_by_symbol(username)

    async def get_all(self) -> list[Record]:
        return await self.__records.get_all()

    async def get_by_id(self, id: int) -> Record | None:
        return await self.__records.get_by_id(id)

    async def add(self, entity: Record) -> None:
        return await self.__records.add(entity)

    async def update(self, entity: Record) -> None:
        return await self.__records.update(entity)

    async def delete(self, id: int) -> None:
        return await self.__records.delete(id)
