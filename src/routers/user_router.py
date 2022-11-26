from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, HTTPException, Header, Depends

from dependencies import admin_only, verify_jwt
from data import ApplicationDbContext
from models import User
from services import UserAuthService


class UserRouter:
    def __init__(self, db: ApplicationDbContext, auth_service: UserAuthService):
        self.db = db
        self.auth = auth_service

        self.router = APIRouter(prefix="/users", dependencies=[Depends(verify_jwt)])

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
            dependencies=[Depends(admin_only)],
            response_model=list[User],
        )

        self.router.add_api_route(
            "/get/{id}",
            self.get_by_id,
            methods=["GET"],
            description="get a user",
            dependencies=[Depends(admin_only)],
            response_model=Optional[User],
        )

        self.router.add_api_route(
            "/add",
            self.add,
            methods=["POST"],
            description="add a user, admin only.",
            dependencies=[Depends(admin_only)],
            response_model=None,
        )

        self.router.add_api_route(
            "/update",
            self.update,
            methods=["POST"],
            description="update a user, admin only.",
            dependencies=[Depends(admin_only)],
            response_model=None,
        )

        self.router.add_api_route(
            "/delete",
            self.delete,
            methods=["POST"],
            description="delete a user, admin only.",
            dependencies=[Depends(admin_only)],
            response_model=None,
        )

    async def me(self, x_authorization: str = Header()) -> User | None:
        return await self.auth.get_user_from_token(x_authorization)

    async def get_all(self) -> list[User]:
        return await self.db.users.get_all()

    async def get_by_id(self, id: int) -> User | None:
        if (user := await self.db.users.get_by_id(id)) is None:
            raise HTTPException(
                status_code=404,
                detail=f"user with id: {id} could not be found"
            )

        return user

    async def add(self, user: User) -> None:
        print(user)
        await self.db.users.add(user)

    # RISK: potential risk, users can update other users by simply entering a different ID
    # TODO add a way for users to be able to update themselves
    #  but filter for security, limit that they can only update their own data
    #  and not other users data, neither their own role.
    async def update(self, user: User) -> None:
        # TODO error handling, and make code robust
        await self.db.users.update(user)

    async def delete(self, id: int) -> None:
        # TORO return 404 if not found
        await self.db.users.delete(id)
