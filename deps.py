from typing import AsyncIterator

from .db import SessionLocal


async def get_db() -> AsyncIterator:
    async with SessionLocal() as session:
        yield session