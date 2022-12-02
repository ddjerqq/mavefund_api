import asyncio as aio
import pytest

import aiosqlite

from models import User
from services import UserService

loop = aio.new_event_loop()
conn = aiosqlite.connect("test.db")
conn = loop.run_until_complete(conn.__aenter__())
curs = loop.run_until_complete(conn.cursor())
user_service = UserService(conn, curs)


@pytest.mark.asyncio
async def test_get_all():
    users = await user_service.get_all()
    assert len(users) == 1


@pytest.mark.asyncio
async def test_get_by_email():
    user = await user_service.get_by_email("test")
    assert user.id == 1
    assert user.username == "test"
    assert user.email == "test"
    assert user.password_hash == "test"
    assert user.rank == 0


@pytest.mark.asyncio
async def test_get_by_username():
    user = await user_service.get_by_username("test")
    assert user.id == 1
    assert user.username == "test"
    assert user.email == "test"
    assert user.password_hash == "test"
    assert user.rank == 0


@pytest.mark.asyncio
async def test_get_by_id():
    user = await user_service.get_by_id(1)
    assert user.id == 1
    assert user.username == "test"
    assert user.email == "test"
    assert user.password_hash == "test"
    assert user.rank == 0


@pytest.mark.asyncio
async def test_add():
    user = User(
        id=2,
        username="test_add",
        email="test_add",
        password_hash="test",
        rank=0
    )

    await user_service.add(user)
    users = await user_service.get_all()
    assert len(users) == 2

    get_user = await user_service.get_by_id(2)
    assert get_user == user

    await user_service.delete(2)


@pytest.mark.asyncio
async def test_add_existing():
    user = User(
        id=1,
        username="test",
        email="test",
        password_hash="test",
        rank=0
    )

    with pytest.raises(Exception):
        await user_service.add(user)


@pytest.mark.asyncio
async def test_update():
    user = await user_service.get_by_id(1)
    user.username = "test2"
    await user_service.update(user)

    get_user = await user_service.get_by_id(1)
    assert get_user.username == "test2"
    get_user.username = "test"
    await user_service.update(get_user)


@pytest.mark.asyncio
async def test_delete():
    await user_service.delete(1)
    users = await user_service.get_all()

    assert len(users) == 0

    await user_service.add(User(
        id=1,
        username="test",
        email="test",
        password_hash="test",
        rank=0
    ))
