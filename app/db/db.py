from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings
from app.db.models import Base

def get_db_async_url():
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite:///"):
        db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    elif db_url.startswith("psycopg:///"):
        db_url = db_url.replace("psycopg:///", "asyncpg:///")
    return db_url


async_engine = create_async_engine(get_db_async_url(), echo=settings.DEBUG)
async_session = sessionmaker(async_engine, class_=AsyncSession)

sync_engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

async_session_factory = sessionmaker(bind=async_engine, class_=AsyncSession)
sync_session_factory = sessionmaker(sync_engine)



async def get_db() -> AsyncGenerator:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

def get_db_sync() -> Generator[Session]:
    session = sync_session_factory()
    try:
        yield session
    finally:
        session.close()


async def init_db():
    async with async_engine.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)


