import uuid
import re
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Header
from core.security.jwt.jwt_provider import JWTProvider
from core.security.password.password_encoder import PasswordEncoder
from domain.user.service.oauth_service import OauthService
from domain.user.entity.oauth_entity import OauthEntity
from domain.user.repository.oauth_repository import OauthRepository
from domain.user.dto.request.signup_dto_request import SignupDtoRequest
from domain.user.dto.request.signin_dto_request import SigninDtoRequest
from domain.user.dto.response.signup_dto_response import SignupDtoResponse
from domain.user.dto.response.signin_dto_response import SigninDtoResponse
from domain.user.dto.response.refresh_token_dto_response import RefreshTokenDtoResponse


class OauthServiceImpl(OauthService):
    
    # 회원가입 기능
    @staticmethod
    async def signup(dto: SignupDtoRequest, session: AsyncSession) -> SignupDtoResponse:
        
        # 사용자 고유 ID 생성
        user_id = str(uuid.uuid4())

        # 사용자 고유 id 생성 중복 체크
        if await OauthRepository.find_by_user_id(session=session, user_id=user_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="사용자 고유 ID 생성 과정에서 문제가 발생했습니다. 잠시 후 다시시도하세요."
            )        

        # 이메일 중복 체크
        if await OauthRepository.find_by_email(session=session, email=dto.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 등록된 이메일입니다."
            )
        
        # 비밀번호 유효성 검사 (영문, 숫자, 일반적으로 자주 사용되는 특수문자만 허용)
        if not re.compile(r"^[A-Za-z0-9!@#$%^&*()_+\-]+$").match(dto.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="비밀번호는 영어, 숫자, 특수문자만 포함해야 합니다."
            )
        
        # 비밀번호 암호화
        hasd_password = PasswordEncoder.hash_password(password=dto.password)
        
        # 사용자 생성
        user = OauthEntity(
            user_id=user_id,
            username=dto.username,
            email=dto.email,
            password=hasd_password,
            )
        
        # DB에 저장
        saved_user = await OauthRepository.save(session=session, user=user)

        # DTO 반환
        return SignupDtoResponse(
            # id=saved_user.id,
            user_id=saved_user.user_id,
            username=saved_user.username,
            password=saved_user.password,
            email=saved_user.email,
            status_code=status.HTTP_200_OK
            ).model_dump()
    
    # 로그인 기능
    @staticmethod
    async def signin(dto: SigninDtoRequest, session: AsyncSession) -> SigninDtoResponse:
        
        # 사용자 조회
        user = await OauthRepository.find_by_email(session=session, email=dto.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 이메일로 등록된 사용자가 없습니다."
            )

        # 비밀번호 검증
        if not PasswordEncoder.verify_password(plain_password=dto.password, hashed_password=user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="비밀번호가 일치하지 않습니다."
            )

        # JWT 토큰 생성 (로그인 성공 시)
        access_token = JWTProvider.create_access_token(user_id=user.user_id)
        refresh_token = JWTProvider.create_refresh_token(user_id=user.user_id)

        # DB에 토큰 저장 또는 업데이트
        await OauthRepository.update_tokens(
            session=session,
            user_id=user.user_id,
            access_token=access_token,
            refresh_token=refresh_token
        )

        # 다시 조회
        update_user = await OauthRepository.find_by_user_id(session=session, user_id=user.user_id)
        
        # 응답 DTO 반환
        return SigninDtoResponse(
            # id=update_user.id,
            user_id=update_user.user_id,
            username=update_user.username,
            email=update_user.email,
            access_token=update_user.access_token,
            refresh_token=update_user.refresh_token,
            status_code=status.HTTP_200_OK
        ).model_dump()

    # 토큰 재발급
    @staticmethod
    async def refresh_token(refresh_token: str, session: AsyncSession) -> RefreshTokenDtoResponse:
        
        # Refresh Token 검증
        payload = JWTProvider.verify_token(refresh_token)
        user_id = payload.get("sub", None)
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh Token이 유효하지 않습니다."
            )

        # 사용자 조회
        user = await OauthRepository.find_by_user_id(session=session, user_id=user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 사용자가 존재하지 않습니다."
            )

        # DB에 저장된 리프레시 토큰 일치 확인
        if user.refresh_token != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh Token이 일치하지 않습니다."
            )

        # 새로운 Access Token 생성
        new_access_token = JWTProvider.create_access_token(user_id=user.user_id)

        # DB에 Access Token 업데이트
        await OauthRepository.update_tokens(
            session=session,
            user_id=user.user_id,
            access_token=new_access_token,
            refresh_token=user.refresh_token
        )

        # 다시 조회
        update_user = await OauthRepository.find_by_user_id(session=session, user_id=user.user_id)
        
        # 응답 DTO 반환
        return RefreshTokenDtoResponse(
            # id=update_user.id,
            user_id=update_user.user_id,
            username=update_user.username,
            email=update_user.email,
            access_token=update_user.access_token,
            # refresh_token=update_user.refresh_token,
            status_code=status.HTTP_200_OK
        ).model_dump()