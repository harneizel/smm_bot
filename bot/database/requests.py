from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import SQLAlchemyError

from bot.database.models import async_session, User


async def add_user(tg_id: int, name, username):
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            if not user:
                user = User(tg_id=tg_id, name=name, username=username, sub_type="basic", rq_made=0)
                session.add(user)
                await session.commit()
        except SQLAlchemyError as e:
            print('e')


async def get_user(tg_id: int) -> User:
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        return result


async def update_user(user_id: int, **kwargs):
    async with async_session() as session:
        await session.execute(update(User).where(User.user_id == user_id).values(**kwargs))
        await session.commit()


async def delete_user(tg_id: int):
    async with async_session() as session:
        await session.execute(delete(User).where(User.tg_id == tg_id))
        await session.commit()

async def sub_type_basic(tg_id: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(sub_type="basic"))
        await session.commit()


async def sub_type_paid(tg_id: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(sub_type="paid"))
        await session.commit()

async def search_us(usernm):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == usernm))
        return user

async def search_id(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return "no_user"
        else:
            return user


async def plus_rq_made(tg_id: int):
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        rq_made = result.rq_made
        rq_made +=1
        print(f"user: {tg_id} requests: {rq_made}")
        await session.execute(update(User).where(User.tg_id==tg_id).values(rq_made=rq_made))
        await session.commit()

async def ban_user(tg_id: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(sub_type="ban"))
        await session.commit()