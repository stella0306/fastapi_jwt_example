from domain.user.entity.base.base_entity import BaseEntity
from core.config.logging.logger_config import LoggerConfig

# 로거 생성
logger = LoggerConfig.get_logger("domain.entity.oauth_entity")

# 계정 관련 엔티티
class OauthEntity(BaseEntity):
    pass