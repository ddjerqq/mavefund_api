from __future__ import annotations

import asyncpg

from src.models import CompanyInfo
from src.repositories.company_info_repository import CompanyInfoRepository


class CompanyInfoService:
    def __init__(self, pool: asyncpg.Pool):
        self._repo = CompanyInfoRepository(pool)

    async def get_csv_by_ticker(self, ticker: str) -> str | None:
        return await self._repo.get_csv_by_ticker(ticker)

    async def get_all_companies_by_name_or_ticker(self, name_or_ticker: str) -> dict[str, str]:
        return await self._repo.get_all_companies_by_name_or_ticker(name_or_ticker)

    async def get_by_ticker(self, ticker: str) -> CompanyInfo | None:
        return await self._repo.get_by_ticker(ticker)

    async def get_all(self) -> list[CompanyInfo]:
        raise NotImplementedError

    async def get_by_id(self, id: int) -> CompanyInfo | None:
        raise NotImplementedError

    async def add(self, entity: CompanyInfo) -> None:
        raise NotImplementedError

    async def update(self, entity: CompanyInfo) -> None:
        raise NotImplementedError

    async def delete(self, id: int) -> None:
        raise NotImplementedError
