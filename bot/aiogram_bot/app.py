import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from bot.aiogram_bot.misc.filters import register_filters
from bot.aiogram_bot.misc.middlewares import register_middlewares
from bot.database.models import on_startup_database
from bot.utils.config import TG_TOKEN


async def aiogram_on_startup(bot: Bot):
    await on_startup_database()

    bot_info = await bot.get_me()
    logging.info("Bot has been started! -> @" + str(bot_info.username))


def register_routers(dp: Dispatcher):
    """
    Registering routers
    """
    from bot.aiogram_bot.handlers import menu, admin
    dp.include_routers(
        menu.router,
        #admin.router
    )


async def aiogram_start():
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    #register_middlewares(dp)
    #register_filters(dp)

    register_routers(dp)
    await aiogram_on_startup(bot)
    await dp.start_polling(bot)
