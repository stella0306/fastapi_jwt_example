from domain.user.repository.base.base_repository import BaseRepository
from domain.user.entity.profile.profile_entity import ProfileEntity

# 테이블 접근 레이어
class ProfileRepository(BaseRepository):
    entity = ProfileEntity