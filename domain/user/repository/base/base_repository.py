from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from domain.user.entity.base.base_entity import BaseEntity
from typing import TypeVar

# 제네릭 타입 힌트
T = TypeVar("T", bound=BaseEntity)

# 테이블 접근 레이어
class BaseRepository:
    entity = BaseEntity  # 기본 엔티티
    
    # 이메일로 사용자 조회
    @classmethod
    async def find_by_email(cls, session: AsyncSession, email: str) -> T:
        stmt = select(cls.entity).where(cls.entity.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    # 사용자명(username)으로 조회
    @classmethod
    async def find_by_username(cls, session: AsyncSession, username: str) -> T:
        stmt = select(cls.entity).where(cls.entity.username == username)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    # 사용자 고유 id(user_id)으로 조회
    @classmethod
    async def find_by_user_id(cls, session: AsyncSession, user_id: str) -> T:
        stmt = select(cls.entity).where(cls.entity.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    # 새 사용자 저장
    @classmethod
    async def save(cls, session: AsyncSession, user: T) -> T:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    # 이메일 수정
    @classmethod
    async def update_email(cls, session: AsyncSession, user_id: int, new_email: str) -> None:
        stmt = (
            update(cls.entity)
            .where(cls.entity.user_id == user_id)
            .values(email=new_email)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()

    # 이름(username) 수정
    @classmethod
    async def update_username(cls, session: AsyncSession, user_id: int, new_username: str) -> None:
        stmt = (
            update(cls.entity)
            .where(cls.entity.user_id == user_id)
            .values(username=new_username)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()

    # 비밀번호(password) 수정
    @classmethod
    async def update_password(cls, session: AsyncSession, user_id: int, new_password: str) -> None:
        stmt = (
            update(cls.entity)
            .where(cls.entity.user_id == user_id)
            .values(password=new_password)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()

    # Access / Refresh Token 업데이트용 메서드
    @classmethod
    async def update_tokens(cls, session: AsyncSession, user_id: str, access_token: str, refresh_token: str) -> None:
        stmt = (
            update(cls.entity)
            .where(cls.entity.user_id == user_id)
            .values(
                access_token=access_token,
                refresh_token=refresh_token
            )
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()


    # 사용자 삭제
    @classmethod
    async def delete(cls, session: AsyncSession, user_id: int) -> None:
        user = await session.get(cls.entity, user_id)
        if user:
            await session.delete(user)
            await session.commit()
