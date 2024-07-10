from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import SQLAlchemyError

from bot.database.models import async_session, User

# добавление юзера в бд
async def add_user(tg_id: int, name, username):
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            if not user:
                user = User(tg_id=tg_id, name=name, username=username, description='', sub_type="basic", rq_made=0, balance=0,
                            making_sub_date="no_date", tag1='', tag2='', tag3='', tag4='', tag5='', dods='')
                session.add(user)
                await session.commit()
        except SQLAlchemyError as e:
            print('error')


# проверяет есть ли пользоватлель в бд
async def is_user(tg_id: int):
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            if not user:
                return "not_user"
            else:
                return "is_user"
        except SQLAlchemyError as e:
            print('error')


# забирает юзера по его id
async def get_user(tg_id: int) -> User:
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        return result


#
async def update_user(user_id: int, **kwargs):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == user_id).values(**kwargs))
        await session.commit()


#
async def delete_user(tg_id: int):
    async with async_session() as session:
        await session.execute(delete(User).where(User.tg_id == tg_id))
        await session.commit()


# установка обычной подписки юзеру
async def sub_type_basic(tg_id: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(sub_type="basic"))
        await session.commit()


# установка платной подписки юзеру
async def sub_type_paid(tg_id: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(sub_type="paid"))
        await session.commit()


# поиск юзера по юзу
async def search_us(usernm):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == usernm))
        return user


# тоже поиск юзера по id
async def search_id(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return "no_user"
        else:
            return user


# увеличение сделанных юзером запросов
async def plus_rq_made(tg_id: int):
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        rq_made = result.rq_made
        rq_made += 1
        print(f"user: {tg_id} requests: {rq_made}")
        await session.execute(update(User).where(User.tg_id == tg_id).values(rq_made=rq_made))
        await session.commit()


# бан юзера установкой ban в подписке
async def ban_user(tg_id: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(sub_type="ban"))
        await session.commit()


# сброс сделанных запросов для всех пользователей
async def reset_to_zero_requests():
    async with async_session() as session:
        users = (await session.scalars(select(User.tg_id))).all()
        print(users)
        for tg_id in users:
            await session.execute(update(User).where(User.tg_id == tg_id).values(rq_made=0))
        await session.commit()


async def get_user_data(tg_id: int):
    async with async_session() as session:
        user = (await session.execute(
            select(User.description, User.tag1, User.tag2, User.tag3, User.tag4, User.tag5).where(
                User.tg_id == tg_id))).first()
        print(user)
        return user
