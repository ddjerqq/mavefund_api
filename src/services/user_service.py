from __future__ import annotations

import asyncpg

from src.models.user import User
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, pool: asyncpg.Pool):
        self._users = UserRepository(pool)

    async def get_by_username(self, username: str) -> User | None:
        return await self._users.get_by_username(username)

    async def get_by_email(self, email: str) -> User | None:
        return await self._users.get_by_email(email)

    async def get_all(self) -> list[User]:
        return await self._users.get_all()

    async def get_by_id(self, id: int) -> User | None:
        return await self._users.get_by_id(id)

    async def add(self, entity: User) -> None:
        await self._users.add(entity)

    async def update(self, entity: User) -> None:
        await self._users.update(entity)

    async def delete(self, id: int) -> None:
        await self._users.delete(id)
