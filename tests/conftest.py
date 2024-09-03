import asyncio
import pytest
from httpx import AsyncClient, ASGITransport

from database import async_engine, Base
from src.main import app


@pytest.fixture(autouse=True, scope='session')
async def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function', autouse=True)
async def setup_database():
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def async_client():
    async with AsyncClient(transport=ASGITransport(app), base_url='http://127.0.0.1:8000') as client:
        yield client
