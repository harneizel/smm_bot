from aiogram import types

import bot.texts as text
from bot.utils.config import CHANNEL_URL as url

start_inlinekeyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_1, url=url)],
         [types.InlineKeyboardButton(text=text.INLINE_2, callback_data="check_sub")],
    ],
)

