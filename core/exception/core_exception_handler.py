from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, OperationalError
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.config.logging.logger_config import LoggerConfig


# FastAPI 전역 예외 처리 클래스
class CoreExceptionHandler:

    logger = LoggerConfig.get_logger("core.exception.core_exception_handler")

    @staticmethod
    def register(app: FastAPI):

        # 입력 데이터 유효성 검증 실패
        @app.exception_handler(RequestValidationError)
        async def handle_validation_error(request: Request, exc: RequestValidationError):
            msg = exc.errors()[0].get("msg", "요청 데이터의 형식이 올바르지 않습니다.")
            CoreExceptionHandler.logger.error(f"[ValidationError]: '{msg}' (URL: {request.url})")

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": "BAD_REQUEST",
                    "message": f"입력값 검증 실패: {msg}",
                },
            )

        # Pydantic ValidationError (모델 검증 오류)
        @app.exception_handler(ValidationError)
        async def handle_pydantic_error(request: Request, exc: ValidationError):
            msg = str(exc.errors()[0].get("msg", "데이터 유효성 검증 실패"))
            CoreExceptionHandler.logger.error(f"[PydanticError]: '{msg}' (URL: {request.url})")

            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "status": "VALIDATION_ERROR",
                    "message": f"요청 데이터가 유효하지 않습니다: {msg}",
                },
            )

        # SQL 제약 조건 위반 (IntegrityError)
        @app.exception_handler(IntegrityError)
        async def handle_integrity_error(request: Request, exc: IntegrityError):
            CoreExceptionHandler.logger.error(f"[IntegrityError]: '{exc}' (URL: {request.url})")

            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "status": "CONFLICT",
                    "message": "데이터베이스에 이미 존재하는 데이터입니다.",
                },
            )

        # DB 연결 실패 (OperationalError)
        @app.exception_handler(OperationalError)
        async def handle_db_connection_error(request: Request, exc: OperationalError):
            CoreExceptionHandler.logger.error(f"[OperationalError]: '{exc}' (URL: {request.url})")

            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": "DB_ERROR",
                    "message": "데이터베이스 연결에 문제가 발생했습니다. 잠시 후 다시 시도해주세요.",
                },
            )

        # 잘못된 인자나 로직 오류
        @app.exception_handler(ValueError)
        async def handle_value_error(request: Request, exc: ValueError):
            CoreExceptionHandler.logger.error(f"[ValueError]: '{exc}' (URL: {request.url})")

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": "BAD_REQUEST",
                    "message": str(exc) or "잘못된 요청입니다.",
                },
            )

        # 인증 실패 또는 권한 부족
        @app.exception_handler(PermissionError)
        async def handle_permission_error(request: Request, exc: PermissionError):
            CoreExceptionHandler.logger.error(f"[PermissionError]: '{exc}' (URL: {request.url})")

            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": "UNAUTHORIZED",
                    "message": "인증이 실패했거나 권한이 없습니다.",
                },
            )

        # HTTPException (FastAPI/Starlette 기본 예외)
        @app.exception_handler(StarletteHTTPException)
        async def handle_http_exception(request: Request, exc: StarletteHTTPException):
            CoreExceptionHandler.logger.error(f"[HTTPException]: '{exc.detail}' (URL: {request.url})")

            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "status": "HTTP_ERROR",
                    "message": exc.detail or "HTTP 요청 처리 중 오류가 발생했습니다.",
                },
            )

        # 처리되지 않은 예외 (서버 내부 오류)
        @app.exception_handler(Exception)
        async def handle_unhandled_exception(request: Request, exc: Exception):
            CoreExceptionHandler.logger.error(f"[UnhandledException]: '{type(exc).__name__}': {exc} (URL: {request.url})")

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": "SERVER_ERROR",
                    "message": "서버 내부에서 예기치 못한 오류가 발생했습니다.",
                },
            )
