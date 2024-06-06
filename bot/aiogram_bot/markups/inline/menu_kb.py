from aiogram import types

import bot.texts as text
from bot.utils.config import CHANNEL_URL as url

start_inlinekeyboard = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_1, url=url)],
         [types.InlineKeyboardButton(text=text.INLINE_2, callback_data="check_sub")],
    ],
)

menu_kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_3, callback_data="dialogue")],
         [types.InlineKeyboardButton(text=text.INLINE_4, callback_data="profile")],
    ],
)

back = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_5, callback_data="new_dialogue")],
         [types.InlineKeyboardButton(text=text.INLINE_6, callback_data="back")],
    ],
)

profile = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_7, callback_data="bye_sub")],
         [types.InlineKeyboardButton(text=text.INLINE_6, callback_data="back")],
    ],
)

end_chat = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_15, callback_data="end_chat")]
    ],
)