import uuid
import re
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Header, Request
from fastapi.responses import JSONResponse
from core.security.jwt.jwt_provider import JWTProvider
from core.security.password.argon2_password_hasher import Argon2PasswordHasher
from domain.user.service.oauth.oauth_service import OauthService
from domain.user.entity.oauth.oauth_entity import OauthEntity
from domain.user.repository.oauth.oauth_repository import OauthRepository
from domain.user.dto.request.oauth.signup_dto_request import SignupDtoRequest
from domain.user.dto.request.oauth.signin_dto_request import SigninDtoRequest
from domain.user.dto.response.oauth.signup_dto_response import SignupDtoResponse
from domain.user.dto.response.oauth.signin_dto_response import SigninDtoResponse
from domain.user.dto.response.oauth.refresh_token_dto_response import RefreshTokenDtoResponse
from core.config.environment.environment_config import environment_config
from core.security.cookie.cookie_util import CookieUtil


class OauthServiceImpl(OauthService):
    
    # 회원가입 기능
    @staticmethod
    async def signup(dto: SignupDtoRequest, session: AsyncSession) -> JSONResponse:
        
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
        hasd_password = Argon2PasswordHasher.hash_password(password=dto.password)
        
        # 사용자 생성
        user = OauthEntity(
            user_id=user_id,
            username=dto.username,
            email=dto.email,
            password=hasd_password,
            )
        
        # DB에 저장
        saved_user = await OauthRepository.save(session=session, user=user)

        # 응답 dto 객체 생성
        response = SignupDtoResponse(
            user_id=saved_user.user_id,
            username=saved_user.username,
            password=saved_user.password,
            email=saved_user.email,
            status_code=status.HTTP_200_OK
            ).model_dump()
        
        # Response 반환
        return JSONResponse(
            content=response,
            status_code=response.get("status_code", 500)
        )
    
    # 로그인 기능
    @staticmethod
    async def signin(dto: SigninDtoRequest, session: AsyncSession) -> JSONResponse:
        
        # 사용자 조회
        user = await OauthRepository.find_by_email(session=session, email=dto.email)
        
        refresh_token = user.refresh_token
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 이메일로 등록된 사용자가 없습니다."
            )

        # 비밀번호 검증
        if not Argon2PasswordHasher.verify_password(plain_password=dto.password, hashed_password=user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="비밀번호가 일치하지 않습니다."
            )

        # JWT 토큰 생성 (로그인 성공 시)
        # 기존에는 refresh_token도 함께 업데이트했으나, 이제는 기존 refresh_token을 그대로 유지한다.
        access_token = JWTProvider.create_access_token(user_id=user.user_id)
        refresh_token = user.refresh_token
        
        # refresh_token 유효성 체크
        try:
            JWTProvider.verify_token(token=refresh_token)
            # 유효하면 그대로 사용
            
        except ValueError:
            # 만료 또는 유효하지 않으면 새로 생성
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
        
        # 응답 dto 생성
        response = SigninDtoResponse(
            user_id=update_user.user_id,
            username=update_user.username,
            email=update_user.email,
            access_token=update_user.access_token,
            refresh_token=update_user.refresh_token,
            status_code=status.HTTP_200_OK
        ).model_dump()
        
        
        # Response 객체 생성
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
            max_age=60 * 60 * 24 * environment_config.refresh_token_expire,
            path="/"
        )
        
        # Response 반환
        return json_response

    # 토큰 재발급
    @staticmethod
    async def refresh_token(request: Request, session: AsyncSession) -> JSONResponse:
        
        # 쿠키에서 토큰 가져오기
        refresh_token = CookieUtil.get_cookie(request=request, key="refresh_token")

        # 토큰 검사
        if refresh_token is None:
            raise ValueError("Refresh token이가 cookie에 없습니다.")
        
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
        
        # 응답 Dto 생성
        response = RefreshTokenDtoResponse(
            user_id=update_user.user_id,
            username=update_user.username,
            email=update_user.email,
            access_token=update_user.access_token,
            status_code=status.HTTP_200_OK
        ).model_dump()
        
        # Response 반환
        return JSONResponse(
            content=response,
            status_code=response.get("status_code", 500)
        )