from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, HTTPException, Header, Depends
from src.data import ApplicationDbContext
from src.models.user import User
from src.services import UserAuthService


class UserRouter:
    unauthorized = HTTPException(status_code=401, detail="invalid authorization header")

    def __init__(self, db: ApplicationDbContext, auth_service: UserAuthService):
        self.db = db
        self.auth = auth_service

        self.router = APIRouter(prefix="/users", dependencies=[Depends(self.verify_jwt)])

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
            dependencies=[Depends(self.admin_only)],
            response_model=list[User],
        )

        self.router.add_api_route(
            "/get/{id}",
            self.get_by_id,
            methods=["GET"],
            description="get a user",
            dependencies=[Depends(self.admin_only)],
            response_model=Optional[User],
        )

        self.router.add_api_route(
            "/add",
            self.add,
            methods=["POST"],
            description="add a user, admin only.",
            dependencies=[Depends(self.admin_only)],
            response_model=None,
        )

        self.router.add_api_route(
            "/update",
            self.update,
            methods=["POST"],
            description="update a user, admin only.",
            dependencies=[Depends(self.admin_only)],
            response_model=None,
        )

        self.router.add_api_route(
            "/delete",
            self.delete,
            methods=["POST"],
            description="delete a user, admin only.",
            dependencies=[Depends(self.admin_only)],
            response_model=None,
        )

    def verify_jwt(self, x_authorization: str = Header()):
        if x_authorization is None:
            raise self.unauthorized

        if (claims := self.auth.extract_claims_from_jwt(x_authorization)) is None:
            raise self.unauthorized

        if "sub" not in claims or "exp" not in claims:
            raise self.unauthorized

    async def admin_only(self, x_authorization: str = Header()) -> None:
        user = await self.auth.get_user_from_token(x_authorization)
        if user is None or user.rank < 3:
            raise HTTPException(status_code=403, detail="admin only")

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
    async def update(self, user: User) -> None:
        # TODO error handling, and make code robust
        await self.db.users.update(user)

    async def delete(self, id: int) -> None:
        # TORO return 404 if not found
        await self.db.users.delete(id)
