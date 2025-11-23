from abc import ABC, abstractmethod
from fastapi import Header, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

class ProfileService(ABC):
    
    # 프로필 조회 추상화
    @abstractmethod
    async def me(request: Request, session: AsyncSession) -> JSONResponse:
        pass
    