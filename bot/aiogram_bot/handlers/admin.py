from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.aiogram_bot.markups.inline.admin_kb import *
from bot.aiogram_bot.misc.states import AdminState
from bot.database import requests as rq
from bot.utils.config import CHANNEL_ID, PAYMENTS_TOKEN, PRICE, BASIC_LIMIT, PAID_LIMIT, ADMIN_IDS
import bot.aiogram_bot.markups.inline.menu_kb as inline_kb
from bot.texts import *
from bot.aiogram_bot.misc.filters.filters import *
admin_ids = [6419408258]
router = Router()

# админ панель
@router.message(F.text == "/admin", IsAdmin())
async def admin_panel(message: Message, bot: Bot):
    await message.answer(TEXT_16, reply_markup=admin)

# поиск пользователей
@router.callback_query(F.data == "search_user" or F.data == "back_to_search")
async def search_user(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text=text.TEXT_17, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=search)

# возвращние в админ панель
@router.callback_query(F.data == "adm_back")
async def sadm_back(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text=text.TEXT_16, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=admin)

# поиск пользователей по юзернейму
@router.callback_query(F.data == "search_us")
async def sadm_back(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text=text.TEXT_18, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=adm_back)
    await state.set_state(AdminState.username)

# поиск пользователей по id
@router.callback_query(F.data == "search_id")
async def sadm_back(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text=text.TEXT_19, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=adm_back)
    await state.set_state(AdminState.user_id)

@router.message(AdminState.username)
async def get_username(message: Message, state: FSMContext):
    user = await rq.search_us(message.text)
    if user.sub_type == "basic":
        sub = "бесплатная"
        limit = BASIC_LIMIT
    elif user.sub_type == "paid":
        sub = "платная"
        limit = PAID_LIMIT
    await message.answer(text=f"""Имя: {user.name}\n"""
                              f"""Тг ID: {user.tg_id}\n"""
                              f"""Юзернейм: {user.username}\n"""
                              f"""Подписка: {sub}\n"""
                              f"""Запросов израсходовано: {user.rq_made}/{limit}""",
                         reply_markup=adm_back)

