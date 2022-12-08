from __future__ import annotations

import asyncpg

from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.services.service_base import ServiceBase


class UserService(ServiceBase):
    def __init__(self, connection: asyncpg.Connection):
        self.__users = UserRepository(connection)

    async def get_by_username(self, username: str) -> User | None:
        return await self.__users.get_by_username(username)

    async def get_by_email(self, email: str) -> User | None:
        return await self.__users.get_by_email(email)

    async def get_all(self) -> list[User]:
        return await self.__users.get_all()

    async def get_by_id(self, id: int) -> User | None:
        return await self.__users.get_by_id(id)

    async def add(self, entity: User) -> None:
        await self.__users.add(entity)

    async def update(self, entity: User) -> None:
        await self.__users.update(entity)

    async def delete(self, id: int) -> None:
        await self.__users.delete(id)
