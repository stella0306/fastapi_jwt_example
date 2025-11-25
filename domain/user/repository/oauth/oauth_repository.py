from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from domain.user.repository.base.base_repository import BaseRepository
from domain.user.entity.oauth.oauth_entity import OauthEntity
from typing import Any, Mapping, TypeVar

# 제네릭 타입 힌트
T = TypeVar("T", bound=OauthEntity)

# 테이블 접근 레이어
class OauthRepository(BaseRepository):
    entity = OauthEntity