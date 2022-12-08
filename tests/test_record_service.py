import pytest

import asyncpg
from services import RecordService


async def get_record_service() -> RecordService:
    pool = await asyncpg.create_pool(user='postgres', password='password', database='mavefund_test', host='localhost')
    return RecordService(pool)


@pytest.mark.asyncio
async def test_get_all():
    record_service = await get_record_service()
    await record_service.get_all()


@pytest.mark.asyncio
async def test_get_all_by_symbol():
    record_service = await get_record_service()
    await record_service.get_all_by_symbol("test")


@pytest.mark.asyncio
async def test_get_by_id():
    record_service = await get_record_service()
    await record_service.get_by_id(1)


@pytest.mark.asyncio
async def test_add():
    record_service = await get_record_service()
    record = await record_service.get_by_id(1)
    record.id = 2

    await record_service.add(record)

    await record_service.delete(2)


@pytest.mark.asyncio
async def test_add_existing():
    record_service = await get_record_service()
    record = await record_service.get_by_id(1)

    with pytest.raises(Exception):
        await record_service.add(record)


@pytest.mark.asyncio
async def test_update():
    record_service = await get_record_service()
    record = await record_service.get_by_id(1)
    record.symbol = "test"
    await record_service.update(record)

    get_record = await record_service.get_by_id(1)

    # reset
    get_record.symbol = "test"
    await record_service.update(get_record)


@pytest.mark.asyncio
async def test_delete():
    record_service = await get_record_service()
    record = await record_service.get_by_id(1)

    await record_service.delete(1)
    rec = await record_service.get_by_id(1)
    assert rec is None

    await record_service.add(record)
