from __future__ import annotations

import asyncpg

from src.models import CompanyInfo
from src.utilities.csv_parser import CsvDataParser
from src.utilities import get_stock_price


class CompanyInfoRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.__pool = pool

    async def get_csv_by_ticker(self, ticker: str) -> str | None:
        async with self.__pool.acquire(timeout=60) as conn:
            conn: asyncpg.Connection
            csv: str | None = await conn.fetchval("""
            SELECT content
            FROM csv_data
            WHERE
                ticker = $1
            """, ticker.upper())

            return csv

    async def get_all_companies_by_name_or_ticker(self, name_or_ticker: str) -> dict[str, str]:
        q = f"%{name_or_ticker}%"

        async with self.__pool.acquire(timeout=60) as conn:
            company_names = await conn.fetch("""
            SELECT ticker, company_name
            FROM csv_data
            WHERE company_name ILIKE $1
            """, q)

            ticker_companies = await conn.fetch("""
            SELECT ticker, company_name
            FROM csv_data
            WHERE ticker ILIKE $1
            """, q)

            return {
                symbol: company_name
                for symbol, company_name in company_names + ticker_companies
            }

    async def get_by_ticker(self, ticker: str) -> CompanyInfo | None:
        ticker = ticker.upper()

        async with self.__pool.acquire(timeout=60) as conn:
            conn: asyncpg.Connection
            row = await conn.fetchrow("""
            SELECT *
            FROM csv_data
            WHERE
                ticker = $1
            """, ticker)

            if row is None:
                return None

            info = await CsvDataParser.parse(db_data=row)
            stock_prices = await get_stock_price(ticker)
            info.stock_prices = list(map(lambda price: round(price, 2), stock_prices.values()))
            return info

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
