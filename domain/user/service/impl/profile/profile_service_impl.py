import uuid
import re
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Header, Request
from fastapi.responses import JSONResponse
from core.security.jwt.jwt_provider import JWTProvider
from core.security.jwt.jwt_filter import JWTFilter
from core.security.password.argon2_password_hasher import Argon2PasswordHasher
from domain.user.service.profile.profile_service import ProfileService
from domain.user.repository.profile.profile_repository import ProfileRepository
from domain.user.dto.request.profile.profile_update_dto_request import ProfileUpdateDtoRequest
from domain.user.dto.response.profile.profile_dto_response import ProfileDtoResponse
from core.config.environment.environment_config import environment_config
from core.security.cookie.cookie_util import CookieUtil

class ProfileServiceImpl(ProfileService):
    
    # 프로필 조회
    @staticmethod
    async def me(request: Request, session: AsyncSession) -> JSONResponse:
        
        # Bearer 헤더 검증
        token = JWTFilter.resolve_token(request=request)
        
        # jwt 검증
        payload = JWTProvider.verify_token(token=token)
        user_id = payload.get("sub", None)
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access Token이 유효하지 않습니다."
            )

        # 사용자 조회
        user = await ProfileRepository.find_by_user_id(session=session, user_id=user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 사용자가 존재하지 않습니다."
            )
        
        # 응답 Dto 생성
        response = ProfileDtoResponse(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            bio=user.bio,
            status_code=status.HTTP_200_OK
        ).model_dump()
        
        # Response 반환
        return JSONResponse(
            content=response,
            status_code=response.get("status_code", 500)
        )

    # 프로필 업데이트
    async def update(request: Request, dto: ProfileUpdateDtoRequest, session: AsyncSession) -> JSONResponse:
        # Bearer 헤더 검증
        token = JWTFilter.resolve_token(request=request)
        
        # jwt 검증
        payload = JWTProvider.verify_token(token=token)
        user_id = payload.get("sub", None)
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access Token이 유효하지 않습니다."
            )

        # 사용자 조회
        user = await ProfileRepository.find_by_user_id(session=session, user_id=user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 사용자가 존재하지 않습니다."
            )
        
        # 자기소개 (bio) 내용 변경
        await ProfileRepository.update_bio(session=session, user_id=user.user_id, new_bio=dto.bio)
        
        # 다시 조회
        update_user = await ProfileRepository.find_by_user_id(session=session, user_id=user.user_id)
        
        # 응답 Dto 생성
        response = ProfileDtoResponse(
            user_id=update_user.user_id,
            username=update_user.username,
            email=update_user.email,
            bio=update_user.bio,
            status_code=status.HTTP_200_OK
        ).model_dump()
        
        # Response 반환
        return JSONResponse(
            content=response,
            status_code=response.get("status_code", 500)
        )