from pydantic import BaseModel, ConfigDict, EmailStr, Field

# 회원가입 응답 Dto
class SignupDtoResponse(BaseModel):
    user_id: str = Field(..., description="생성된 사용자 고유 id")
    status_code: int = Field(..., description="HTTP 상태 코드")
    
    # 모델 설정
    model_config = ConfigDict(from_attributes=True)