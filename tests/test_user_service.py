import random

import pytest

import asyncpg

from models import User
from services import UserService


async def get_user_service() -> UserService:
    conn = await asyncpg.connect(user='postgres', password='password', database='mavefund_test', host='localhost')
    return UserService(conn)



@pytest.mark.asyncio
async def test_get_all():
    user_service = await get_user_service()
    users = await user_service.get_all()


@pytest.mark.asyncio
async def test_get_by_email():
    user_service = await get_user_service()
    await user_service.get_by_email("test")


@pytest.mark.asyncio
async def test_get_by_username():
    user_service = await get_user_service()
    await user_service.get_by_username("test")


@pytest.mark.asyncio
async def test_get_by_id():
    user_service = await get_user_service()
    await user_service.get_by_id(1)


@pytest.mark.asyncio
async def test_add():
    user_service = await get_user_service()
    user = User(
        id=random.randint(1, 100000),
        username="test",
        email="test",
        password_hash="test",
        rank=0
    )
    await user_service.add(user)
    await user_service.delete(user.id)


@pytest.mark.asyncio
async def test_add_existing():
    user_service = await get_user_service()
    user = User(
        id=10,
        username="test",
        email="test",
        password_hash="test",
        rank=0
    )

    await user_service.add(user)

    with pytest.raises(Exception):
        await user_service.add(user)

    await user_service.delete(10)


@pytest.mark.asyncio
async def test_update():
    user_service = await get_user_service()
    user = await user_service.get_by_id(1)
    user.username = "test2"
    await user_service.update(user)

    get_user = await user_service.get_by_id(1)
    assert get_user.username == "test2"
    get_user.username = "test"
    await user_service.update(get_user)


@pytest.mark.asyncio
async def test_delete():
    user_service = await get_user_service()
    await user_service.delete(1)
    await user_service.get_all()

    await user_service.add(User(
        id=1,
        username="test",
        email="test",
        password_hash="test",
        rank=0
    ))
