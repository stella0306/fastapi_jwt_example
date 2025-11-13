from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# CORS 정책 설정 클래스
class CORSMiddlewareConfig:

    ALLOW_ORIGINS: list[str] = ["*"] # 허용할 Origin (출처)
    ALLOW_METHODS: list[str] = ["*"] # 허용할 HTTP 메서드 목록
    ALLOW_HEADERS: list[str] = ["*"] # 허용할 요청 헤더 목록
    ALLOW_CREDENTIALS: bool = True # 자격 증명(쿠키, 인증정보) 허용 여부

    # CORS 미들웨어 등록
    @staticmethod
    def register(app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=CORSMiddlewareConfig.ALLOW_ORIGINS,
            allow_credentials=CORSMiddlewareConfig.ALLOW_CREDENTIALS,
            allow_methods=CORSMiddlewareConfig.ALLOW_METHODS,
            allow_headers=CORSMiddlewareConfig.ALLOW_HEADERS,
        )
