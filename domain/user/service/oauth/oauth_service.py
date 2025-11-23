from abc import ABC, abstractmethod
from fastapi import Header, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from domain.user.dto.request.oauth.signup_dto_request import SignupDtoRequest
from domain.user.dto.request.oauth.signin_dto_request import SigninDtoRequest

class OauthService(ABC):
    
    # 회원가입 추상화
    @abstractmethod
    async def signup(dto: SignupDtoRequest, session: AsyncSession) -> JSONResponse:
        pass
    
    # 로그인 추상화
    @abstractmethod
    async def signin(dto: SigninDtoRequest, session: AsyncSession) -> JSONResponse:
        pass
    
    # 토큰 재발급 추상화
    @abstractmethod
    async def refresh_token(request: Request, session: AsyncSession) -> JSONResponse:
        pass
    