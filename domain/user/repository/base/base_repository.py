from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from domain.user.entity.base.base_entity import BaseEntity
from typing import Any, Mapping, TypeVar

# 제네릭 타입 힌트
T = TypeVar("T", bound=BaseEntity)

# 테이블 접근 레이어
class BaseRepository:
    entity = BaseEntity  # 기본 엔티티
    
    # 공통 메서드
    @classmethod
    async def find_one_by(cls, session: AsyncSession, **filters) -> T | None:
        stmt = select(cls.entity).filter_by(**filters)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def update_one_by_id(cls, session: AsyncSession, user_id: int, **values) -> None:
        stmt = (
            update(cls.entity)
            .where(cls.entity.user_id == user_id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()


    # 이메일로 사용자 조회
    @classmethod
    async def find_by_email(cls, session: AsyncSession, email: str) -> T | None:
        return await cls.find_one_by(session=session, email=email)

    # 사용자명(username)으로 조회
    @classmethod
    async def find_by_username(cls, session: AsyncSession, username: str) -> T | None:
        return await cls.find_one_by(session=session, username=username)

    # 사용자 고유 id(user_id)으로 조회
    @classmethod
    async def find_by_user_id(cls, session: AsyncSession, user_id: str) -> T | None:
        return await cls.find_one_by(session=session, user_id=user_id)


    # 이메일 수정
    @classmethod
    async def update_email(cls, session: AsyncSession, user_id: int, new_email: str) -> None:
        await cls.update_one_by_id(session=session, user_id=user_id, email=new_email)

    # 이름(username) 수정
    @classmethod
    async def update_username(cls, session: AsyncSession, user_id: int, new_username: str) -> None:
        await cls.update_one_by_id(session=session, user_id=user_id, username=new_username)

    # 비밀번호(password) 수정
    @classmethod
    async def update_password(cls, session: AsyncSession, user_id: int, new_password: str) -> None:
        await cls.update_one_by_id(session=session, user_id=user_id, password=new_password) 
        
    # Access / Refresh Token 업데이트용 메서드
    @classmethod
    async def update_tokens(cls, session: AsyncSession, user_id: str, access_token: str, refresh_token: str) -> None:
        await cls.update_one_by_id(session=session, user_id=user_id, access_token=access_token, refresh_token=refresh_token) 

    # 사용자 소개 (bio) 수정
    @classmethod
    async def update_bio(cls, session: AsyncSession, user_id: int, new_bio: str) -> None:
        await cls.update_one_by_id(session=session, user_id=user_id, bio=new_bio) 

    # 새 사용자 저장
    @classmethod
    async def save(cls, session: AsyncSession, user: T) -> T | None:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    # 사용자 삭제
    @classmethod
    async def delete(cls, session: AsyncSession, user_id: int) -> None:
        user = await session.get(cls.entity, user_id)
        if user:
            await session.delete(user)
            await session.commit()
