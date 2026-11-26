from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True)

async_conversation_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_conversation_factory() as conversation:
        yield conversation
