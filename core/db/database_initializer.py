from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.db.database import Database
from core.db.base import Base
from core.config.logger_config import LoggerConfig

# DB 초기화 및 연결 검증을 담당하는 클래스
class DatabaseInitializer:

    # 로거 정의
    logger = LoggerConfig.get_logger("core.db.database_initializer")

    @staticmethod
    @asynccontextmanager
    async def db_lifespan(app: FastAPI):
        DatabaseInitializer.logger.info("데이터베이스 초기화 시작")

        try:
            async with Database.engine.begin() as conn:
                # 테이블 생성
                await conn.run_sync(Base.metadata.create_all)
            DatabaseInitializer.logger.info("데이터베이스 연결 성공")
            
        except Exception as e:
            DatabaseInitializer.logger.exception(f"데이터베이스 연결 실패: {e}")

        yield  # 애플리케이션 실행 중
        DatabaseInitializer.logger.info("데이터베이스 세션 종료 및 자원 정리 완료")
