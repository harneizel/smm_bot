from aiogram import types

import bot.texts as text

main_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [types.KeyboardButton(text=text.REPLY_1)],
        [types.KeyboardButton(text=text.REPLY_1)]
    ]
)
