from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic


T = TypeVar("T")


class RepositoryBase(ABC, Generic[T]):
    @abstractmethod
    async def get_all(self) -> list[T]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> T | None:
        pass

    @abstractmethod
    async def add(self, entity: T) -> None:
        pass

    @abstractmethod
    async def update(self, entity: T) -> None:
        pass

    @abstractmethod
    async def delete(self, entity: T) -> None:
        pass
