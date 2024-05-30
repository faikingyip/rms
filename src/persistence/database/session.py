from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.configuration import Configuration

DATABASE_URL = Configuration.PERSISTENCE__DATABASE__DATABASE_URL

# Create a database engine
engine = create_async_engine(DATABASE_URL)

# Declare a sessionmaker with autocommit and autoflush settings
SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


class Base(DeclarativeBase):
    pass


async def create_database_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def async_session_scope() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()
