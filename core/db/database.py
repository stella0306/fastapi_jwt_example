from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config.settings import settings
from typing import AsyncGenerator


# 비동기 SQLAlchemy 엔진 및 세션 관리를 담당하는 클래스
class Database:
    # 데이터베이스 엔진 생성
    engine = create_async_engine(
        url=settings.async_db_url,
        echo=True,
    )

    # 세션 팩토리(sessionmaker) 설정
    async_session_factory = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # FastAPI 의존성 주입용 정적 세션 메서드
    @staticmethod
    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        async with Database.async_session_factory() as session:
            yield session