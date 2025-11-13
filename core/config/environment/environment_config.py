import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Final

# .env 파일 로드
load_dotenv()

# 실행 환경 설정
class EnvironmentConfig(BaseModel):
    # JWT 정의
    jwt_secret: str = os.getenv("JWT_SECRET", "devsecret")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire: int = int(os.getenv("ACCESS_TOKEN_EXPIRE", "30"))
    refresh_token_expire: int = int(os.getenv("REFRESH_TOKEN_EXPIRE", "7"))

    # 데이터베이스 정의
    db_user: str = os.getenv("DB_USER", "appuser")
    db_password: str = os.getenv("DB_PASSWORD", "apppw")
    db_host: str = os.getenv("DB_HOST", "127.0.0.1")
    db_port: str = os.getenv("DB_PORT", "3306")
    db_name: str = os.getenv("DB_NAME", "appdb")

    # DB URL 정의
    @property
    def async_db_url(self) -> str:
        return f"mysql+asyncmy://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"

# 불변 객체 생성
environment_config: Final[EnvironmentConfig] = EnvironmentConfig()