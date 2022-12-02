import asyncio as aio
import pytest

import aiosqlite
from services import RecordService

loop = aio.new_event_loop()
conn = aiosqlite.connect("test.db")
conn = loop.run_until_complete(conn.__aenter__())
curs = loop.run_until_complete(conn.cursor())
record_service = RecordService(conn, curs)


@pytest.mark.asyncio
async def test_get_all():
    records = await record_service.get_all()
    assert len(records) == 1


@pytest.mark.asyncio
async def test_get_all_by_symbol():
    records = await record_service.get_all_by_symbol("test")
    assert len(records) == 1


@pytest.mark.asyncio
async def test_get_by_id():
    record = await record_service.get_by_id(1)
    assert record.id == 1


@pytest.mark.asyncio
async def test_add():
    record = await record_service.get_by_id(1)
    record.id = 2
    await record_service.add(record)
    users = await record_service.get_all()
    assert len(users) == 2

    get_record = await record_service.get_by_id(2)
    assert get_record == record

    await record_service.delete(1)


@pytest.mark.asyncio
async def test_add_existing():
    record = await record_service.get_by_id(1)
    with pytest.raises(Exception):
        await record_service.add(record)


@pytest.mark.asyncio
async def test_update():
    record = await record_service.get_by_id(1)
    record.username = "test2"
    await record_service.update(record)

    get_record = await record_service.get_by_id(1)
    assert get_record.username == "test2"
    get_record.username = "test"
    await record_service.update(get_record)


@pytest.mark.asyncio
async def test_delete():
    record = await record_service.get_by_id(1)
    await record_service.delete(1)
    records = await record_service.get_all()
    assert len(records) == 0

    await record_service.add(record)
