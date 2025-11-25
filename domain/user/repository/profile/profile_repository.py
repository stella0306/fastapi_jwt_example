from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from domain.user.repository.base.base_repository import BaseRepository
from domain.user.entity.profile.profile_entity import ProfileEntity
from typing import Any, Mapping, TypeVar

# 제네릭 타입 힌트
T = TypeVar("T", bound=ProfileEntity)

# 테이블 접근 레이어
class ProfileRepository(BaseRepository):
    entity = ProfileEntity