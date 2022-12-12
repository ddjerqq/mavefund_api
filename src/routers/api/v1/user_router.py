from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, HTTPException, Request, Depends

from src.data import ApplicationDbContext
from src.models import User
from src.dependencies.auth import admin_only


class UserRouter:
    FORBIDDEN = HTTPException(status_code=403, detail=f"you do not have access to this data.")

    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(
            prefix="/users",
            dependencies=[Depends(admin_only)],
        )

        self.router.add_api_route(
            "/@me",
            self.me,
            methods=["GET"],
            description="get the current user",
            response_model=Optional[User],
        )

        self.router.add_api_route(
            "/get/all",
            self.get_all,
            methods=["GET"],
            description="get all users",
            response_model=list[User],
        )

        self.router.add_api_route(
            "/get/{id}",
            self.get_by_id,
            methods=["GET"],
            description="get a user",
            response_model=Optional[User],
        )

        self.router.add_api_route(
            "/add",
            self.add,
            methods=["POST"],
            description="add a user, admin only.",
            response_model=None,
        )

        self.router.add_api_route(
            "/update",
            self.update,
            methods=["PUT"],
            description="update a user, admin only.",
            response_model=None,
        )

        self.router.add_api_route(
            "/delete",
            self.delete,
            methods=["DELETE"],
            description="delete a user, admin only.",
            response_model=None,
        )

    async def me(self, req: Request) -> User | None:
        return req.user

    async def get_all(self, req: Request) -> list[User]:
        if req.user.rank != 3:
            raise self.FORBIDDEN

        return await self.db.users.get_all()

    async def get_by_id(self, req: Request, id: int) -> User | None:
        if req.user.rank != 3:
            raise self.FORBIDDEN

        if (user := await self.db.users.get_by_id(id)) is None:
            raise HTTPException(
                status_code=404,
                detail=f"user with id: {id} could not be found"
            )

        return user

    async def add(self, req: Request, user: User) -> None:
        if req.user.rank != 3:
            raise self.FORBIDDEN

        await self.db.users.add(user)

    # RISK: potential risk, users can update other users by simply entering a different ID
    # TODO add a way for users to be able to update themselves
    #  but filter for security, limit that they can only update their own data
    #  and not other users data, neither their own role.
    async def update(self, req: Request, user: User) -> None:
        if req.user.rank != 3:
            raise self.FORBIDDEN

        # TODO error handling, and make code robust
        await self.db.users.update(user)

    async def delete(self, req: Request, id: int) -> None:
        if req.user.rank != 3:
            raise self.FORBIDDEN

        # TODO return 404 if not found
        await self.db.users.delete(id)
