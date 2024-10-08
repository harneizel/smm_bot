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
        [types.InlineKeyboardButton(text=text.INLINE_4, callback_data="profile")]
        #[types.InlineKeyboardButton(text=text.INLINE_4, web_app=types.WebAppInfo(url='https://147.45.246.252:80/app'))] # пока не доделано
    ],
) # https://harneizel.github.io/webapp.github.io/

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

back_to_menu = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_6, callback_data="back")]
    ],
)

end_chat = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_15, callback_data="end_chat")]
    ],
)

rules_approval = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=text.INLINE_20, callback_data="agree")]
    ],
)

web_app =  types.InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[
        [types.InlineKeyboardButton(text='Мой профиль', web_app=types.WebAppInfo(url=f'https://ya.ru/'))]
    ],
)
