from pydantic import BaseModel, ConfigDict, EmailStr, Field

# 회원가입 응답 Dto
class SignupDtoResponse(BaseModel):
    # id: int = Field(..., description="생성된 사용자 순서 id (자동 증가)")
    user_id: str = Field(..., description="생성된 사용자 고유 id")
    username: str = Field(..., description="사용자 이름")
    password: str = Field(..., description="사용자 비밀번호")
    email: EmailStr = Field(..., description="사용자 이메일")
    status_code: int = Field(..., description="HTTP 상태 코드")
    
    # 모델 설정
    model_config = ConfigDict(from_attributes=True)