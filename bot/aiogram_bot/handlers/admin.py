from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.database import requests as rq
from bot.utils.config import CHANNEL_ID, PAYMENTS_TOKEN, PRICE, BASIC_LIMIT, PAID_LIMIT, ADMIN_IDS
import bot.aiogram_bot.markups.inline.inline_kb as inline_kb
import bot.texts as text
from bot.aiogram_bot.misc.filters.filters import *
admin_ids = [6419408258]
router = Router()

@router.message(F.text == "/admin", IsAdmin())
async def admin_panel(message: Message, bot: Bot):
    await message.answer('Вы зашли в админ панель')