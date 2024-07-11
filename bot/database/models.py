from sqlalchemy import BigInteger, event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from bot.utils.config import SQLALCHEMY_URL

engine = create_async_engine(SQLALCHEMY_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, nullable=False)  # айти в тг
    name: Mapped[str] = mapped_column(nullable=False)  # имя в тг
    username: Mapped[str] = mapped_column(nullable=True)  # тг юз
    description: Mapped[str] = mapped_column(nullable=True)
    sub_type: Mapped[str] = mapped_column(nullable=False)  # basic, paid, ban
    rq_made: Mapped[int] = mapped_column(nullable=False)  # кол во сделанных запросов в день
    balance: Mapped[int] = mapped_column(nullable=False)  # баланс юзера
    making_sub_date: Mapped[str] = mapped_column(nullable=True)  # дата оформления подписки
    tag1: Mapped[str] = mapped_column(nullable=True)  # теги юзера
    tag2: Mapped[str] = mapped_column(nullable=True)
    tag3: Mapped[str] = mapped_column(nullable=True)
    tag4: Mapped[str] = mapped_column(nullable=True)
    tag5: Mapped[str] = mapped_column(nullable=True)
    dods: Mapped[str] = mapped_column(nullable=True)  # давно отложенные дела

# общий счетчик всех диалогов, нужен для conversation_id у coze
class Sessions(Base):
    __tablename__ = 'sessions'
    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(nullable=True)

# созадет в sessions счетчик при создании бд
async def after_create_sessions():
    async with async_session() as session:
        async with session.begin():
            new_session = Sessions(id=1, conversation_id=1)
            session.add(new_session)
            await session.commit()

# Привязка функции-обработчика к событию after_create для таблицы Sessions
event.listen(Sessions.__table__, 'after_create', await after_create_sessions)

async def on_startup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
