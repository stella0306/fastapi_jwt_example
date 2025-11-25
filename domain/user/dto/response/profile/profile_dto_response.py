from pydantic import BaseModel, ConfigDict, EmailStr, Field

# 프로필 조회 응답 Dto
class ProfileDtoResponse(BaseModel):
    user_id: str = Field(..., description="생성된 사용자 고유 id")
    username: str = Field(..., description="사용자 이름")
    email: EmailStr = Field(..., description="사용자 이메일")
    bio: str = Field(..., description="사용자 소개")
    status_code: int = Field(..., description="HTTP 상태 코드")
    
    # 모델 설정
    model_config = ConfigDict(from_attributes=True)