import logging

from aiogram import Dispatcher, Bot, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.methods import DeleteWebhook

from bot.aiogram_bot.misc.filters import register_filters
from bot.aiogram_bot.misc.middlewares.middlewares import *
from bot.database.models import on_startup_database
from bot.utils.config import TG_TOKEN, CHANNEL_ID
from bot.aiogram_bot.misc.filters.filters import IsAdmin
from bot.aiogram_bot.handlers.admin import admin_panel

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
        admin.router,
    )


#def register_filters(dp):


async def aiogram_start():
    bot = Bot(token=TG_TOKEN, default=DefaultBotProperties(parse_mode='Markdown'))
    dp = Dispatcher(storage=MemoryStorage())

    # register_middlewares(dp)
    #register_filters(dp)


    dp.update.outer_middleware(SubsriptionMiddleware(bot, channel_id=CHANNEL_ID))

    #dp.update.outer_middleware(UnsubscribeMiddleware())

    register_routers(dp)
    await aiogram_on_startup(bot)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await bot.delete_webhook()
    await dp.start_polling(bot)
