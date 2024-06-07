from aiogram import types

import bot.texts as text
from bot.utils.config import CHANNEL_URL as url


admin = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_8, callback_data="search_user")],
        [types.InlineKeyboardButton(text=text.INLINE_9, callback_data="get_db")],
    ],
)

search = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_10, callback_data="search_us")],
        [types.InlineKeyboardButton(text=text.INLINE_11, callback_data="search_id")],
        [types.InlineKeyboardButton(text=text.INLINE_12, callback_data="adm_back")],
    ],
)

adm_back = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_12, callback_data="back_to_search")],
    ],
)

user_actions = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_13, callback_data="transform_sub_type"),
        types.InlineKeyboardButton(text=text.INLINE_14, callback_data="ban_user")],
        [types.InlineKeyboardButton(text=text.INLINE_12, callback_data="back_to_search")]
    ],
)