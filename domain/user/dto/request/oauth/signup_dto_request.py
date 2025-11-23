from pydantic import BaseModel, ConfigDict, EmailStr, Field

# 회원가입 요청 Dto
class SignupDtoRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50, description="사용자 이름")
    email: EmailStr = Field(..., description="사용자 이메일 주소")
    password: str = Field(..., min_length=4, max_length=255, description="사용자 비밀번호")
    
    # 모델 설정
    model_config = ConfigDict(from_attributes=True)