from pydantic import BaseModel, ConfigDict, EmailStr, Field

# 로그인 응답 Dto
class SigninDtoResponse(BaseModel):
    user_id: str = Field(..., description="생성된 사용자 고유 id")
    username: str = Field(..., description="사용자 이름")
    email: EmailStr = Field(..., description="사용자 이메일")
    access_token: str = Field(..., description="Access Token")
    refresh_token: str = Field(..., description="Refresh Token")
    status_code: int = Field(..., description="HTTP 상태 코드")
    
    # 모델 설정
    model_config = ConfigDict(from_attributes=True)