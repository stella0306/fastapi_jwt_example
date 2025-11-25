from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.database import Database
from domain.user.service.impl.profile.profile_service_impl import ProfileServiceImpl
from domain.user.dto.request.profile.profile_update_dto_request import ProfileUpdateDtoRequest

# 프로필 라우터 구현
class ProfileController:
    def __init__(self):
        
        # 라우터 인스턴스 셍성
        self.router = APIRouter(prefix="/profile", tags=["user"])
        
        # 라우터 등록
        self.router.add_api_route(
            path="/me",
            endpoint=self.me,
            methods=["get"]
        )

        self.router.add_api_route(
            path="/update",
            endpoint=self.update,
            methods=["put"]
        )
        
    # 프로필 조회 | Depends를 사용하여 의존성 주입
    async def me(self, request: Request, session: AsyncSession = Depends(Database.get_session)) -> JSONResponse:
        response = await ProfileServiceImpl.me(request=request, session=session)
        
        # 반환
        return response
    
    
    # 프로필 수정 | Depends를 사용하여 의존성 주입
    async def update(self, request: Request, dto: ProfileUpdateDtoRequest, session: AsyncSession = Depends(Database.get_session)) -> JSONResponse:
        response = await ProfileServiceImpl.update(request=request, dto=dto, session=session)
        
        # 반환
        return response