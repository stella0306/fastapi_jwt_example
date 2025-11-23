from fastapi import Request, HTTPException, status

# jwt 토큰 검증을 담당하는 클래스
class JWTFilter:
    
    # Bearer 헤더 검증
    @staticmethod
    def resolve_token(request: Request) -> str:
        header = request.headers.get("Authorization")

        if not header or not header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization 헤더가 누락되었거나 잘못되었습니다.",
            )

        return header[7:]  # "Bearer " 제거