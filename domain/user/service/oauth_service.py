from abc import ABC, abstractmethod
from fastapi import Header
from sqlalchemy.ext.asyncio import AsyncSession
from domain.user.dto.request.signup_dto_request import SignupDtoRequest
from domain.user.dto.request.signin_dto_request import SigninDtoRequest
from domain.user.dto.response.signup_dto_response import SignupDtoResponse
from domain.user.dto.response.signin_dto_response import SigninDtoResponse
from domain.user.dto.response.refresh_token_dto_response import RefreshTokenDtoResponse

class OauthService(ABC):
    
    # 회원가입 추상화
    @abstractmethod
    async def signup(dto: SignupDtoRequest, session: AsyncSession) -> SignupDtoResponse:
        pass
    
    # 로그인 추상화
    @abstractmethod
    async def signin(dto: SigninDtoRequest, session: AsyncSession) -> SigninDtoResponse:
        pass
    
    # 토큰 재발급 추상화
    @abstractmethod
    async def refresh_token(refresh_token: str, session: AsyncSession) -> RefreshTokenDtoResponse:
        pass
    