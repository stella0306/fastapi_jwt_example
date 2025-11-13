from fastapi import Request, Response
from typing import Optional

# 쿠키를 유틸리티입니다.
class CookieUtil:

    # 쿠키 저장
    @staticmethod
    def set_cookie(
        response: Response,
        key: str,
        value: str,
        max_age: int,
        http_only: bool = True,
        secure: bool = True,
        same_site: str = "Strict",
        path: str = "/"
    ):
        response.set_cookie(
            key=key,
            value=value,
            max_age=max_age,
            httponly=http_only,
            secure=secure,
            samesite=same_site,
            path=path
        )

    # 쿠키 삭제
    @staticmethod
    def delete_cookie(
        response: Response,
        name: str,
        path: str = "/"
    ):
        response.delete_cookie(
            key=name,
            path=path
        )

    # 쿠키 가져오기
    @staticmethod
    def get_cookie(request: Request, key: str) -> Optional[str]:
        return request.cookies.get(key, None)
