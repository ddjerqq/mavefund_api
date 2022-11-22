from __future__ import annotations

from fastapi import Depends

from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.services.service_base import ServiceBase


class UserService(ServiceBase):
    def __init__(self, user_repository: UserRepository = Depends()):
        self.__users = user_repository

    async def get_all(self) -> list[User]:
        return await self.__users.get_all()

    async def get_by_id(self, id: int) -> User | None:
        return await self.__users.get_by_id(id)

    async def add(self, entity: User) -> None:
        await self.__users.add(entity)
        await self.__users.save_changes()

    async def update(self, entity: User) -> None:
        await self.__users.update(entity)
        await self.__users.save_changes()

    async def delete(self, entity: User) -> None:
        await self.__users.delete(entity)
        await self.__users.save_changes()
