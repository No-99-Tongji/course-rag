from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .auth import hash_password
from .config import ADMIN_BOOTSTRAP_PASSWORD, ADMIN_BOOTSTRAP_USERNAME, DATABASE_URL
from .models import Admin, Base

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await bootstrap_admin()


async def close_db() -> None:
    await engine.dispose()


async def bootstrap_admin() -> None:
    if not ADMIN_BOOTSTRAP_PASSWORD:
        return
    async with SessionLocal() as session:
        result = await session.execute(select(Admin).where(Admin.username == ADMIN_BOOTSTRAP_USERNAME))
        if result.scalar_one_or_none() is not None:
            return
        session.add(Admin(username=ADMIN_BOOTSTRAP_USERNAME, password_hash=hash_password(ADMIN_BOOTSTRAP_PASSWORD)))
        await session.commit()
