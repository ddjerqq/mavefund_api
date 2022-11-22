from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException

from src.data import ApplicationDbContext
from src.models.user import User


class UserRouter:
    def __init__(self, db: ApplicationDbContext):
        self.db = db

        self.router = APIRouter(prefix="/users")

        self.router.add_api_route("/get/all", self.get_all, methods=["GET"], response_model=list[User])
        self.router.add_api_route("/get/{id}", self.get_by_id, methods=["GET"], response_model=User)
        self.router.add_api_route("/add", self.add, methods=["POST"])
        self.router.add_api_route("/update", self.update, methods=["PUT"])
        self.router.add_api_route("/delete/{id}", self.delete, methods=["DELETE"])

    # TODO add this after we add authentication and authorization using Token model
    # @router.get("/users/me", tags=["users"], response_model=User)
    # async def read_users_me(
    #         current_user: User = Depends(get_current_user)
    # ) -> User:
    #     if current_user:
    #         return current_user
    #     else:
    #         raise HTTPException(status_code=401, detail="unauthorized")

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

    async def update(self, user: User) -> None:
        # TODO error handling, and make code robust
        await self.db.users.update(user)

    async def delete(self, id: int) -> None:
        # TORO return 404 if not found
        await self.db.users.delete(id)
