# Взят из проекта, под доработку
import logging
import traceback

from aiogram import Router, types, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from bot.aiogram_bot.markups.reply.main_menu import get_main_menu
from bot.aiogram_bot.services.admin_service import send_log

router = Router()


@router.error()
async def error_handler(event: types.ErrorEvent = None, exception: Exception = None, state: FSMContext = None):
    exception = exception or event.exception
    data = ""

    if event:
        data = str(event.update.message)
        if state:
            state_data = await state.get_data()
            state_current = await state.get_state()
            full_state_data = str(state_data) + "\n" + str(state_current)
            data += "\n\n" + full_state_data
            await state.clear()
        data += "\n\n"
        message = event.update.callback_query or event.update.message

        user_id = message.from_user.id
        bot: Bot = message.bot

        text_to_send = "Произошла ошибка! Приносим свои извининения, администрация уже работает над исправлением. Попробуйте ещё раз позднее."

        try:
            await bot.send_message(user_id,
                                   text_to_send,
                                   reply_markup=get_main_menu(message), reply_to_message_id=message.message_id)
        except TelegramBadRequest as ex:
            if 'not found' in ex.message:
                await bot.send_message(user_id,
                                       text_to_send,
                                       reply_markup=get_main_menu(message))

    error_text = "".join((traceback.format_exception(None, exception, exception.__traceback__)))

    full_log_text = data + error_text
    try:
        await send_log(full_log_text, title_file=type(exception).__name__,
                       description_file=str(exception))
    except TelegramBadRequest as ex:
        if 'chat not found' in ex.message:
            logging.error(full_log_text)
        else:
            raise ex
