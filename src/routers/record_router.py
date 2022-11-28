from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, HTTPException, Header, Depends

from dependencies import admin_only, verify_jwt
from data import ApplicationDbContext
from models import Record
from services import UserAuthService


class RecordRouter:
    def __init__(self, db: ApplicationDbContext, auth_service: UserAuthService):
        self.db = db
        self.auth = auth_service

        self.router = APIRouter(prefix="/records", dependencies=[Depends(verify_jwt)])

        self.router.add_api_route(
            "/get/all",
            self.get_all,
            methods=["GET"],
            description="get all records",
            dependencies=[Depends(admin_only)],
            response_model=list[Record],
        )

        self.router.add_api_route(
            "/get/{id}",
            self.get_by_id,
            methods=["GET"],
            description="get a record",
            dependencies=[Depends(admin_only)],
            response_model=Optional[Record],
        )

        self.router.add_api_route(
            "/add",
            self.add,
            methods=["POST"],
            description="add a record, admin only.",
            dependencies=[Depends(admin_only)],
            response_model=None,
        )

        self.router.add_api_route(
            "/update",
            self.update,
            methods=["PUT"],
            description="update a record, admin only.",
            dependencies=[Depends(admin_only)],
            response_model=None,
        )

        self.router.add_api_route(
            "/delete",
            self.delete,
            methods=["DELETE"],
            description="delete a record, admin only.",
            dependencies=[Depends(admin_only)],
            response_model=None,
        )

    async def get_all(self) -> list[Record]:
        return await self.db.records.get_all()

    async def get_by_id(self, id: int) -> Record | None:
        if (user := await self.db.records.get_by_id(id)) is None:
            raise HTTPException(
                status_code=404,
                detail=f"user with id: {id} could not be found"
            )

        return user

    async def add(self, user: Record) -> None:
        await self.db.records.add(user)

    # RISK: potential risk, users can update other users by simply entering a different ID
    # TODO add a way for users to be able to update themselves
    #  but filter for security, limit that they can only update their own data
    #  and not other users data, neither their own role.
    async def update(self, user: Record) -> None:
        # TODO error handling, and make code robust
        await self.db.users.update(user)

    async def delete(self, id: int) -> None:
        # TODO return 404 if not found
        await self.db.users.delete(id)