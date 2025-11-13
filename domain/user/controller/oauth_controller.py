from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from domain.user.dto.request.signup_dto_request import SignupDtoRequest
from domain.user.dto.request.signin_dto_request import SigninDtoRequest 
from domain.user.service.impl.oauth_service_impl import OauthServiceImpl
from core.db.database import Database
from core.security.cookie.cookie_util import CookieUtil
from core.config.settings import settings

# 사용자 라우터 구현
class OauthController:
    def __init__(self):
        
        # 라우터 인스턴스 셍성
        self.router = APIRouter(prefix="/oauth", tags=["Auth"])
        
        # 라우터 등록
        self.router.add_api_route(
            path="/signup",
            endpoint=self.signup,
            methods=["post"]
        )

        # 라우터 등록
        self.router.add_api_route(
            path="/signin",
            endpoint=self.signin,
            methods=["post"]
        )

        # 라우터 등록
        self.router.add_api_route(
            path="/refresh",
            endpoint=self.refresh_token,
            methods=["post"]
        )
        
    # 회원가입 | Depends를 사용하여 의존성 주입
    async def signup(self, dto: SignupDtoRequest, session: AsyncSession = Depends(Database.get_session)) -> JSONResponse:
        response = await OauthServiceImpl.signup(dto=dto, session=session)
        
        return JSONResponse(
            content=response,
            status_code=response.get("status_code", 500)
        )
        
    # 로그인 | Depends를 사용하여 의존성 주입
    async def signin(self, dto: SigninDtoRequest, session: AsyncSession = Depends(Database.get_session)) -> JSONResponse:
        response = await OauthServiceImpl.signin(dto=dto, session=session)
        
        # 먼저 Response 객체 생성
        json_response = JSONResponse(
            content=response,
            status_code=response.get("status_code", 500)
        )

        # 쿠키 설정
        CookieUtil.set_cookie(
            response=json_response,
            key="refresh_token",
            value=response["refresh_token"],
            http_only=True,
            secure=True,
            same_site="strict",
            max_age=60 * 60 * 24 * settings.refresh_token_expire,
            path="/"
        )
        
        #  반환
        return json_response

    # 토큰 재발급 | Depends를 사용하여 의존성 주입
    async def refresh_token(self, request: Request, session: AsyncSession = Depends(Database.get_session)) -> JSONResponse:
        # 쿠키에서 토큰 가져오기
        refresh_token = CookieUtil.get_cookie(request=request, key="refresh_token")

        # 토큰 검사
        if refresh_token is None:
            raise ValueError("Refresh token이가 cookie에 없습니다.")
    
        response = await OauthServiceImpl.refresh_token(refresh_token=refresh_token, session=session)
        return JSONResponse(
            content=response,
            status_code=response.get("status_code", 500)
        )