import jwt
from datetime import datetime, timedelta, timezone
from core.config.environment.environment_config import environment_config

# Access / Refresh 토큰 발급 및 검증
class JWTProvider:

    @staticmethod
    # Access Token 생성
    def create_access_token(user_id: str) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(
                hours=environment_config.access_token_expire
            )
        }
        return jwt.encode(payload=payload, key=environment_config.jwt_secret, algorithm=environment_config.jwt_algorithm)

    # Refresh Token 생성
    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(
                days=environment_config.refresh_token_expire
            )
        }
        
        return jwt.encode(payload=payload, key=environment_config.jwt_secret, algorithm=environment_config.jwt_algorithm)

    # JWT 검증
    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                jwt=token,
                key=environment_config.jwt_secret,
                algorithms=environment_config.jwt_algorithm,
            )
            return payload
        
        except jwt.ExpiredSignatureError:
            raise ValueError("토큰이 만료되었습니다.")
        
        except jwt.InvalidTokenError:
            raise ValueError("유효하지 않은 토큰입니다.")
