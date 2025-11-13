import jwt
from datetime import datetime, timedelta, timezone
from core.config.settings import settings

# Access / Refresh 토큰 발급 및 검증
class JWTService:

    @staticmethod
    # Access Token 생성
    def create_access_token(user_id: str) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(
                hours=settings.access_token_expire
            )
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    # Refresh Token 생성
    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(
                hours=settings.refresh_token_expire
            )
        }
        
        return jwt.encode(payload=payload, key=settings.jwt_secret, algorithm=settings.jwt_algorithm)

    # JWT 검증
    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
            return payload
        
        except jwt.ExpiredSignatureError:
            raise ValueError("토큰이 만료되었습니다.")
        
        except jwt.InvalidTokenError:
            raise ValueError("유효하지 않은 토큰입니다.")
