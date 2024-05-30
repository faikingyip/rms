from contextlib import asynccontextmanager
from typing import AsyncGenerator
from unittest.mock import AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.persistence.database.session import Base


def mock_async_session_scope_factory():

    mock_async_session = AsyncMock()
    mock_async_session.commit = AsyncMock()
    mock_async_session.rollback = AsyncMock()
    mock_async_session.refresh = AsyncMock()

    @asynccontextmanager
    async def mock_async_session_scope():
        async with mock_async_session:
            yield mock_async_session

    return mock_async_session_scope, mock_async_session


# ===== in memory database setup =====

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
    # poolclass=StaticPool,
)


async def setup_test_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def reset_test_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


TestingSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@asynccontextmanager
async def async_testing_session_scope() -> AsyncGenerator[AsyncSession, None]:

    async with TestingSessionLocal() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()
