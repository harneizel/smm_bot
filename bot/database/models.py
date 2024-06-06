from sqlalchemy import BigInteger, JSON
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from bot.utils.config import SQLALCHEMY_URL

engine = create_async_engine(SQLALCHEMY_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger) # айти в тг
    name: Mapped[str] = mapped_column() # имя в тг
    username: Mapped[str] = mapped_column() # тг юз
    sub_type: Mapped[str] = mapped_column() #basic, paid, ban
    history = mapped_column(JSON) # история сообщений в диалоге
    rq_made: Mapped[int] = mapped_column() # кол во сделанных запросов в день



async def on_startup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
