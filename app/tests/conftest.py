from uuid import uuid4

import pytest
import pytest_asyncio
from database.session import get_db_session
from httpx import ASGITransport, AsyncClient
from main import app, gen_uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from .mock_data.seed_data import insert_mock_data

engine = create_async_engine(url="sqlite+aiosqlite:///:memory:")
test_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_test_session_override():
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://tests"
    ) as async_client:
        yield async_client


@pytest.fixture(scope="session")
def test_id():
    return str(uuid4())


@pytest_asyncio.fixture(scope="session")
async def provider_token(client: AsyncClient):
    response = await client.post(
        "/provider/authentication",
        data={"username": "vijayalabs@gmail.com", "password": "password123"},
    )

    return response.json()["access_token"]


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_and_teardown(test_id: str):
    print("\n🧪 Starting tests..")
    app.dependency_overrides[gen_uuid] = lambda: test_id
    app.dependency_overrides[get_db_session] = get_test_session_override

    async with engine.begin() as conn:
        from database.claim_sql_model import Claims, PlaceOfService, Provider  # noqa: F401

        await conn.run_sync(SQLModel.metadata.create_all)

    # Insert mock data
    async with test_session() as session:
        await insert_mock_data(session)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    app.dependency_overrides.clear()
    print("\n🏁 Finished!")

@pytest.fixture(autouse=True)
def mock_redis_blacklist(monkeypatch):
    async def token_not_blacklisted(jti: str) -> bool:
        return False

    monkeypatch.setattr("utils.check_jti_in_blacklist", token_not_blacklisted)