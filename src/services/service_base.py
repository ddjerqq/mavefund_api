from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic


T = TypeVar("T")


class ServiceBase(ABC, Generic[T]):
    @abstractmethod
    async def get_all(self) -> list[T]:
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> T | None:
        ...

    @abstractmethod
    async def add(self, entity: T) -> None:
        ...

    @abstractmethod
    async def update(self, entity: T) -> None:
        ...

    @abstractmethod
    async def delete(self, entity: T) -> None:
        ...
