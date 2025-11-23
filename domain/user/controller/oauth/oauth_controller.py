from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from domain.user.dto.request.oauth.signup_dto_request import SignupDtoRequest
from domain.user.dto.request.oauth.signin_dto_request import SigninDtoRequest 
from domain.user.service.impl.oauth.oauth_service_impl import OauthServiceImpl
from core.db.database import Database

# 사용자 라우터 구현
class OauthController:
    def __init__(self):
        
        # 라우터 인스턴스 셍성
        self.router = APIRouter(prefix="/oauth", tags=["user"])
        
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
        
        # 반환
        return response
        
    # 로그인 | Depends를 사용하여 의존성 주입
    async def signin(self, dto: SigninDtoRequest, session: AsyncSession = Depends(Database.get_session)) -> JSONResponse:
        response = await OauthServiceImpl.signin(dto=dto, session=session)
        
        #  반환
        return response

    # 토큰 재발급 | Depends를 사용하여 의존성 주입
    async def refresh_token(self, request: Request, session: AsyncSession = Depends(Database.get_session)) -> JSONResponse:
        response = await OauthServiceImpl.refresh_token(request=request, session=session)
        
        # 반환
        return response