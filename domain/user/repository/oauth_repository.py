from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from domain.user.entity.oauth_entity import OauthEntity
from typing import Optional


# Oauth 테이블 접근 레이어
class OauthRepository:
    # 이메일로 사용자 조회
    @staticmethod
    async def find_by_email(session: AsyncSession, email: str) -> Optional[OauthEntity]:
        stmt = select(OauthEntity).where(OauthEntity.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    # 사용자명(username)으로 조회
    @staticmethod
    async def find_by_username(session: AsyncSession, username: str) -> Optional[OauthEntity]:
        stmt = select(OauthEntity).where(OauthEntity.username == username)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    # 사용자 고유 id(user_id)으로 조회
    @staticmethod
    async def find_by_user_id(session: AsyncSession, user_id: str) -> Optional[OauthEntity]:
        stmt = select(OauthEntity).where(OauthEntity.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    # 새 사용자 저장
    @staticmethod
    async def save(session: AsyncSession, user: OauthEntity) -> OauthEntity:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    # 이메일 수정
    @staticmethod
    async def update_email(session: AsyncSession, user_id: int, new_email: str) -> None:
        stmt = (
            update(OauthEntity)
            .where(OauthEntity.user_id == user_id)
            .values(email=new_email)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()

    # 이름(username) 수정
    @staticmethod
    async def update_username(session: AsyncSession, user_id: int, new_username: str) -> None:
        stmt = (
            update(OauthEntity)
            .where(OauthEntity.user_id == user_id)
            .values(username=new_username)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()

    # 비밀번호(password) 수정
    @staticmethod
    async def update_password(session: AsyncSession, user_id: int, new_password: str) -> None:
        stmt = (
            update(OauthEntity)
            .where(OauthEntity.user_id == user_id)
            .values(password=new_password)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()

    # Access / Refresh Token 업데이트용 메서드
    @staticmethod
    async def update_tokens(session: AsyncSession, user_id: str, access_token: str, refresh_token: str) -> None:
        stmt = (
            update(OauthEntity)
            .where(OauthEntity.user_id == user_id)
            .values(
                access_token=access_token,
                refresh_token=refresh_token
            )
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()


    # 사용자 삭제
    @staticmethod
    async def delete(session: AsyncSession, user_id: int) -> None:
        user = await session.get(OauthEntity, user_id)
        if user:
            await session.delete(user)
            await session.commit()
