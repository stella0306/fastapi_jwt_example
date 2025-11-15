from passlib.context import CryptContext

# 비밀번호 해싱 및 검증 서비스
class Argon2PasswordHasher:

    # argon2 알고리즘 사용
    pwd_context = CryptContext(
        schemes=["argon2"],
        deprecated="auto",
        argon2__type="id",
        argon2__memory_cost=102400,   # 100 MB
        argon2__time_cost=4,          # 연산 난이도
        argon2__parallelism=2         # 병렬 스레드
    )
    
    # 비밀번호를 argon2 해시로 변환
    @staticmethod
    def hash_password(password: str) -> str:
        return Argon2PasswordHasher.pwd_context.hash(secret=password)

    # 입력된 비밀번호가 해시와 일치하는지 검증
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return Argon2PasswordHasher.pwd_context.verify(secret=plain_password, hash=hashed_password)
