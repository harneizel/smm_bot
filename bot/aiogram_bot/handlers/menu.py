from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext

from bot.utils.config import CHANNEL_ID
import bot.aiogram_bot.markups.inline.inline_kb as inline_kb
import bot.texts as text

router = Router()


@router.message(F.text == "/start")
async def start_btn(message: types.Message, state: FSMContext):
    await message.answer(text=text.START_TEXT, reply_markup=inline_kb.start_inlinekeyboard)

@router.message()
async def check(message: types.Message):
    await message.answer(message.text)

@router.callback_query(F.data == "check_sub")
async def asdf(call: types.CallbackQuery, bot: Bot):
    print(CHANNEL_ID)
    user_ch_status = await bot.get_chat_member(chat_id=f"@{CHANNEL_ID}", user_id=call.from_user.id)
    if user_ch_status.status != 'left':
        await call.message.answer(text.TEXT_1)
    else:
        await call.answer(text.TEXT_2)
