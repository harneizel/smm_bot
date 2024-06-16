from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.aiogram_bot.markups.inline.admin_kb import *
from bot.aiogram_bot.misc.states import AdminState
from bot.database import requests as rq
from bot.utils.config import CHANNEL_ID, PAYMENTS_TOKEN, PRICE, BASIC_LIMIT, PAID_LIMIT, ADMIN_IDS
import bot.aiogram_bot.markups.inline.menu_kb as inline_kb
from bot.texts import *
from bot.aiogram_bot.misc.filters.filters import *
router = Router()

def form_text(user):
    if user.sub_type == "basic":
        sub = "бесплатная"
        limit = BASIC_LIMIT
        text1 = INLINE_13
        text2 = INLINE_14
        cb_1 = f"set_paid_{user.tg_id}"
        cb_2 = f"ban_user_{user.tg_id}"
    elif user.sub_type == "paid":
        limit = PAID_LIMIT
        sub = "платная"
        text1 = INLINE_18
        text2 = INLINE_14
        cb_1 = f"set_basic_{user.tg_id}"
        cb_2 = f"ban_user_{user.tg_id}"
    elif user.sub_type == "ban":
        sub = "забанен"
        limit = 0
        text1 = INLINE_19
        text2 = INLINE_17
        cb_1 = f"no_data"
        cb_2 = f"unban_user_{user.tg_id}"

    text = f"""Имя: {user.name}\n"""\
           f"""Тг ID: {user.tg_id}\n"""\
           f"""Юзернейм: {user.username}\n"""\
           f"""Подписка: {sub}\n"""\
           f"""Запросов израсходовано: {user.rq_made}/{limit}"""

    return text, sub, limit, text1, text2, cb_1, cb_2

def user_kb_builder(text1, text2, cb_1,cb_2):
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    builder.add(types.InlineKeyboardButton(text=text1, callback_data=cb_1), # подписка
                types.InlineKeyboardButton(text=text2, callback_data=cb_2), # бан / разбан
                types.InlineKeyboardButton(text=text.INLINE_12, callback_data=f"back_to_search"))
    return builder

# админ панель
@router.message(F.text == "/admin", IsAdmin())
async def admin_panel(message: Message, bot: Bot):
    await message.answer(TEXT_16, reply_markup=admin)

# поиск пользователей
@router.callback_query(F.data == "search_user")
async def search_user(call: CallbackQuery, bot: Bot):
    await bot.edit_message_text(text=text.TEXT_17, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=search)

@router.callback_query(F.data=="back_to_search")
async def back_to_search(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
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
    await bot.edit_message_text(text=text.TEXT_18, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=adm_back)
    await state.set_state(AdminState.username)

# поиск пользователей по id
@router.callback_query(F.data == "search_id")
async def sadm_back(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text=text.TEXT_19, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=adm_back)
    await state.set_state(AdminState.user_id)

@router.message(AdminState.username)
async def get_username(message: Message, state: FSMContext):
    user = await rq.search_us(str(message.text))
    if user == "no_user":
        await message.answer(TEXT_22, reply_markup=adm_back)
    else:
        us_text, sub, limit, text1, text2, cb_1, cb_2 = form_text(user)
        await state.clear()
        builder = user_kb_builder(text1, text2, cb_1, cb_2)

        await message.answer(text=us_text,
                             reply_markup=builder.as_markup())

@router.message(AdminState.user_id)
async def get_username(message: Message, state: FSMContext):
    user = await rq.search_id(int(message.text))
    if user == "no_user":
        await message.answer(TEXT_22, reply_markup=adm_back)
    else:
        us_text, sub, limit, text1, text2, cb_1, cb_2 = form_text(user)
        await state.clear()
        builder = user_kb_builder(text1, text2, cb_1, cb_2)
        await message.answer(text=us_text,
                             reply_markup=builder.as_markup())

@router.callback_query(F.data[0:7] == "back_to")
async def ban_user(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id=int(call.data[8:])
    user = await rq.search_id(int(user_id))
    if user == "no_user":
        await bot.edit_message_text(text=TEXT_22, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    reply_markup=adm_back)
    else:
        us_text, sub, limit, text1, text2, cb_1, cb_2 = form_text(user)
        await state.clear()
        builder = user_kb_builder(text1, text2, cb_1, cb_2)
        await bot.edit_message_text(text=us_text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    reply_markup=builder.as_markup())

@router.callback_query(F.data[0:9] == "set_basic")
async def ban_user(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.data[10:]
    print(f"Установка бесплатной подписки для {user_id}")
    await rq.sub_type_basic(user_id)
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    builder.add(types.InlineKeyboardButton(text=text.INLINE_16, callback_data=f"back_to_{user_id}"))
    await bot.edit_message_text(text=f"{text.TEXT_24}{user_id}", chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=builder.as_markup())

@router.callback_query(F.data[0:8] == "set_paid")
async def ban_user(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.data[9:]
    print(f"Установка платной подписки для {user_id}")
    await rq.sub_type_paid(user_id)
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    builder.add(types.InlineKeyboardButton(text=text.INLINE_16, callback_data=f"back_to_{user_id}"))
    await bot.edit_message_text(text=f"{text.TEXT_25}{user_id}", chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=builder.as_markup())


@router.callback_query(F.data[0:8] == "ban_user")
async def ban_user(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.data[9:]
    print(f"Бан для {user_id}")
    await bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    builder.add(types.InlineKeyboardButton(text=text.INLINE_16, callback_data=f"back_to_{user_id}"))
    await rq.ban_user(int(user_id))
    await bot.edit_message_text(text=f"{text.TEXT_23}{user_id}", chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=builder.as_markup())


@router.callback_query(F.data[0:10] == "unban_user")
async def ban_user(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.data[11:]
    print(f"Разабан для {user_id}")
    await bot.unban_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    builder.add(types.InlineKeyboardButton(text=text.INLINE_16, callback_data=f"back_to_{user_id}"))
    await rq.sub_type_basic(int(user_id))
    await bot.edit_message_text(text=f"{text.TEXT_26}{user_id}", chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=builder.as_markup())