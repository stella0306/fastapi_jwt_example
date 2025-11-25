from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core.db.base import Base
from core.config.logging.logger_config import LoggerConfig

# 로거 생성
logger = LoggerConfig.get_logger("domain.entity.base_entity")

# DB Table 분리를 위한 base_entity는 추후에 삭제
class BaseEntity(Base):
    # DB 테이블명 정의
    __tablename__ = "fastapi_jwt_example"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True) # 기본키 (자동 증가)
    
    user_id: Mapped[str] = mapped_column(String(length=1000), nullable=False, unique=True) # 사용자 고유 아이디
    username: Mapped[str] = mapped_column(String(length=1000), nullable=False, unique=False) # 사용자 이름
    email: Mapped[str] = mapped_column(String(length=1000), nullable=False, unique=True) # 이메일
    password: Mapped[str] = mapped_column(String(length=1000), nullable=False) # 비밀번호 (암호화된 값)
    bio: Mapped[str] = mapped_column(String(length=1000), nullable=False, unique=False) # 사용자 소개
    
    # JWT 토큰
    access_token: Mapped[str] = mapped_column(String(length=1000), nullable=True)           # Access Token
    refresh_token: Mapped[str] = mapped_column(String(length=1000), nullable=True)          # Refresh Token
    
    