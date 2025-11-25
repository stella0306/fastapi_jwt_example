from abc import ABC, abstractmethod
from fastapi import Header, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from domain.user.dto.request.profile.profile_update_dto_request import ProfileUpdateDtoRequest

class ProfileService(ABC):
    
    # 프로필 조회 추상화
    @abstractmethod
    async def me(request: Request, session: AsyncSession) -> JSONResponse:
        pass
    
    # 프로필 업데이트 추상화
    @abstractmethod
    async def update(request: Request, dto: ProfileUpdateDtoRequest, session: AsyncSession) -> JSONResponse:
        pass