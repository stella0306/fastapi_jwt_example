from domain.user.repository.base.base_repository import BaseRepository
from domain.user.entity.oauth.oauth_entity import OauthEntity

# 테이블 접근 레이어
class OauthRepository(BaseRepository):
    entity = OauthEntity