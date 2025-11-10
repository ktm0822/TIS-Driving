from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from .config import settings

# 비동기 엔진
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)

# 세션팩토리
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(AsyncAttrs, DeclarativeBase):
    """모든 모델의 Base 클래스"""
    pass


async def init_models() -> None:
    """서버 시작 시 테이블 생성"""
    from . import models  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)