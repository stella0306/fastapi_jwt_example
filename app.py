import uvicorn
from fastapi import FastAPI
from core.db.database_initializer import DatabaseInitializer
from core.config.logging.logger_config import LoggerConfig
from core.exception.core_exception_handler import CoreExceptionHandler
from core.middleware.cors_middleware_config import CORSMiddlewareConfig
from domain.user.controller.oauth_controller import OauthController

# 로거 생성
logger = LoggerConfig.get_logger("app")

# FastAPI 앱 생성
app = FastAPI(
    title="FastAPI",
    lifespan=DatabaseInitializer.db_lifespan
)

# 전역 예외처리 적용
CoreExceptionHandler.register(app=app)
# CORS 적용
CORSMiddlewareConfig.register(app=app)

# 컨트롤러 인스턴스 생성
user_controller = OauthController()

# 라우터 등록
app.include_router(router=user_controller.router, prefix="/api")

if __name__ == "__main__":
    logger.info("FastAPI 서버를 시작합니다...")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
