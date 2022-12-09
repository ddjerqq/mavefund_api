import os
import random
import pytest
import asyncpg
from dotenv import load_dotenv

from src.models import User
from src.services import UserService


load_dotenv()


async def get_user_service() -> UserService:
    pool = await asyncpg.create_pool(
        user='postgres',
        password=os.getenv("POSTGRES_PASSWORD"),
        database='postgres',
        host=os.getenv("HOST")
    )
    return UserService(pool)


@pytest.mark.asyncio
async def test_get_all():
    user_service = await get_user_service()
    users = await user_service.get_all()
    assert len(users) > 0


@pytest.mark.asyncio
async def test_get_by_email():
    user_service = await get_user_service()
    user = await user_service.get_by_email("test")
    assert user is not None


@pytest.mark.asyncio
async def test_get_by_username():
    user_service = await get_user_service()
    user = await user_service.get_by_username("test")
    assert user is not None


@pytest.mark.asyncio
async def test_get_by_id():
    user_service = await get_user_service()
    user = await user_service.get_by_id(1)
    assert user is not None


@pytest.mark.asyncio
async def test_add():
    user_service = await get_user_service()
    user = User(
        id=random.randint(1, 100000),
        username=''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
        email=''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)) + '@gmail.com',
        password_hash="test",
        rank=0
    )
    await user_service.add(user)

    get = await user_service.get_by_id(user.id)
    assert get is not None

    await user_service.delete(user.id)


@pytest.mark.asyncio
async def test_add_existing():
    user_service = await get_user_service()
    user = await user_service.get_by_id(1)

    with pytest.raises(Exception):
        await user_service.add(user)


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
    user = await user_service.get_by_id(1)

    await user_service.delete(user.id)

    get_user = await user_service.get_by_id(1)
    assert get_user is None

    await user_service.add(user)
