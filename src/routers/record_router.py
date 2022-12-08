from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, HTTPException, Request

from ..data import ApplicationDbContext
from ..models import Record


class RecordRouter:
    FORBIDDEN = HTTPException(status_code=403, detail=f"you do not have access to this data.")

    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(prefix="/records")

        self.router.add_api_route(
            "/get/all",
            self.get_all,
            methods=["GET"],
            description="get all records",
            response_model=list[Record],
        )

        self.router.add_api_route(
            "/get/{id}",
            self.get_by_id,
            methods=["GET"],
            description="get a record",
            response_model=Optional[Record],
        )

        self.router.add_api_route(
            "/add",
            self.add,
            methods=["POST"],
            description="add a record, admin only.",
            response_model=None,
        )

        self.router.add_api_route(
            "/update",
            self.update,
            methods=["PUT"],
            description="update a record, admin only.",
            response_model=None,
        )

        self.router.add_api_route(
            "/delete",
            self.delete,
            methods=["DELETE"],
            description="delete a record, admin only.",
            response_model=None,
        )

    async def get_all(self, req: Request) -> list[Record]:
        if req.user.rank != 3:
            raise self.FORBIDDEN

        return await self.db.records.get_all()

    async def get_by_id(self, req: Request, id: int) -> Record | None:
        if req.user.rank != 3:
            raise self.FORBIDDEN

        if (record := await self.db.records.get_by_id(id)) is None:
            raise HTTPException(
                status_code=404,
                detail=f"record with id: {id} could not be found"
            )

        return record

    async def add(self, req: Request, record: Record) -> None:
        if req.user.rank != 3:
            raise self.FORBIDDEN

        await self.db.records.add(record)

    async def update(self, req: Request, record: Record) -> None:
        if req.user.rank != 3:
            raise self.FORBIDDEN

        await self.db.users.update(record)

    async def delete(self, req: Request, id: int) -> None:
        if req.user.rank != 3:
            raise self.FORBIDDEN

        await self.db.users.delete(id)
