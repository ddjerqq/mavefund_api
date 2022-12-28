from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, HTTPException, Request, Depends

from src.data import ApplicationDbContext
from src.models import Record
from src.models.dto import Symbol, MinimalRecord
from src.dependencies.auth import subscriber_only, admin_only


class RecordRouter:
    FORBIDDEN = HTTPException(status_code=403, detail=f"you do not have access to this data.")

    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(
            prefix="/records",
            dependencies=[Depends(subscriber_only)],
        )

        self.router.add_api_route(
            "/get/all",
            self.get_all,
            methods=["GET"],
            description="get all symbols.",
            response_model=list[Symbol],
            dependencies=[Depends(admin_only)],
        )

        self.router.add_api_route(
            "/get/{ticker:str}",
            self.get_by_ticker,
            methods=["GET"],
            description="get a symbol by it's ticker.",
            response_model=Optional[Symbol],
        )

        self.router.add_api_route(
            "/add",
            self.add,
            methods=["POST"],
            description="add a record.",
            response_model=None,
            dependencies=[Depends(admin_only)],
        )

        self.router.add_api_route(
            "/update",
            self.update,
            methods=["PUT"],
            description="update a record.",
            response_model=None,
            dependencies=[Depends(admin_only)],
        )

        self.router.add_api_route(
            "/delete/{id:int}",
            self.delete,
            methods=["DELETE"],
            description="delete a record.",
            response_model=None,
            dependencies=[Depends(admin_only)],
        )


    async def get_all(self) -> list[Symbol]:
        records = await self.db.records.get_all()
        ticker_records: dict[str, list[Record]] = {}

        for record in records:
            records_for_current_symbol = ticker_records.setdefault(
                record.symbol,
                [],
            )
            records_for_current_symbol.append(record)

        # possible multiple iteration
        minified_ticker_records = {
            ticker: list(map(MinimalRecord.from_record, records))
            for ticker, records in ticker_records.items()
        }

        symbols = [
            Symbol.from_minimal_records(records)
            for _, records in minified_ticker_records
        ]

        return symbols


    async def get_by_ticker(self, ticker: str) -> Symbol | None:
        records = await self.db.records.get_all_by_symbol(ticker)
        minimal_records = list(map(MinimalRecord.from_record, records))
        symbol = Symbol.from_minimal_records(minimal_records)
        return symbol


    async def add(self, record: Record) -> None:
        await self.db.records.add(record)


    async def update(self, record: Record) -> None:
        await self.db.users.update(record)


    async def delete(self, id: int) -> None:
        await self.db.users.delete(id)
