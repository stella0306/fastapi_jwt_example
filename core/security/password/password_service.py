from passlib.context import CryptContext

# 비밀번호 해싱 및 검증 서비스
class PasswordService:

    # argon2 알고리즘 사용
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    # 비밀번호를 argon2 해시로 변환
    @staticmethod
    def hash_password(password: str) -> str:
        print(len(password))
        return PasswordService.pwd_context.hash(secret=password)

    # 입력된 비밀번호가 해시와 일치하는지 검증
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordService.pwd_context.verify(secret=plain_password, hash=hashed_password)
