from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError

from bot.database.models import async_session, User


async def get_users():
    async with async_session() as session:
        result = await session.scalars(select(User))
        return result


async def add_user(user_id: int, **kwargs) -> User:
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.user_id == user_id))
            if not user:
                user = User(user_id=user_id, **kwargs)
                session.add(user)
                await session.commit()
            return user
        except SQLAlchemyError as e:
            await session.rollback()
            raise e


async def get_user(user_id: int) -> User:
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.user_id == user_id))
        return result


async def update_user(user_id: int, **kwargs):
    async with async_session() as session:
        await session.execute(update(User).where(User.user_id == user_id).values(**kwargs))
        await session.commit()


async def delete_user(user_id: int):
    async with async_session() as session:
        await session.execute(delete(User).where(User.user_id == user_id))
        await session.commit()
