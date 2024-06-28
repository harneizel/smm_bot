from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import hashlib

from bot.database import requests as rq
from bot.utils.config import CHANNEL_ID, PAYMENTS_TOKEN, PRICE, BASIC_LIMIT, PAID_LIMIT, \
    MRH_LOGIN, PASS_1, DESCRIPTION, IS_TEST as is_test, TEST_PASS_1, ROBOKASSA_PAYMENT_URL as robo_url
from bot.utils.util import get_epoch, generate_payment_link
import bot.aiogram_bot.markups.inline.menu_kb as inline_kb
import bot.texts as text
from bot.aiogram_bot.misc.states import *
from bot.utils.coze_requests import *


router = Router()

# отправка печатает... ботом на время генерации нейросетью
async def send_typing_action(chat_id, bot):
    try:
        while True:
            await bot.send_chat_action(chat_id, "typing")
            await asyncio.sleep(4)
    except asyncio.CancelledError:
        pass

# генерация кнопки со ссылкой на оплату
async def payments_button(tg_id, builder):
    price, mrh_login, pass_1, test_pass_1, desc = PRICE, MRH_LOGIN, PASS_1, TEST_PASS_1, DESCRIPTION
    #tg_id = (await rq.get_user(tg_id)).id
    if is_test == 0:
        url = generate_payment_link(merchant_login=mrh_login, merchant_password_1=pass_1, cost=price,
                                    description=desc, is_test=is_test, Shp_id=tg_id, robokassa_payment_url=robo_url)
    elif is_test == 1:
        url = generate_payment_link(merchant_login=mrh_login, merchant_password_1=test_pass_1, cost=price,
                                    description=desc, is_test=is_test, Shp_id=tg_id, robokassa_payment_url=robo_url)


    #crc = hashlib.md5(f"{mrh_login}:{price}::{pass_1}:Shp_id={tg_id}".encode('utf-8')).hexdigest()
    #print(id, crc, tg_id)
    #url = f"https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin={mrh_login}&OutSum={price}&Description={desc}&IsTest=1&Shp_id={tg_id}&SignatureValue={crc}"
    #url = f"https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin={mrh_login}&OutSum={price}&InvID=&Description={desc}&SignatureValue={crc}"

    print(url)
    builder.max_width = 1
    builder.add(InlineKeyboardButton(text=text.INLINE_7, url=url))
    return builder

# главное меню
@router.message(F.text == "/start")
async def start_btn(message: Message, bot: Bot):
    await rq.add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer(text.TEXT_1, reply_markup=inline_kb.menu_kb)


# кнопка я подписался
@router.callback_query(F.data == "check_sub")
async def check_sub(call: CallbackQuery, bot: Bot):
    #await rq.add_user(call.from_user.id, call.from_user.first_name, call.from_user.username)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer(text.TEXT_1, reply_markup=inline_kb.menu_kb)

# согласие с правилами
@router.callback_query(F.data == "agree")
async def check_sub(call: CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer(text=text.START_TEXT, reply_markup=inline_kb.start_inlinekeyboard)

# начало диалога с gpt
@router.callback_query(F.data == "dialogue")
async def dialogue(call: CallbackQuery, bot: Bot, state: FSMContext):
    if not os.path.exists(f"./bot/database/histories/{call.from_user.id}.json"):
        os.mknod(f"./bot/database/histories/{call.from_user.id}.json")
        print("файл создан")
    with open(file=f"./bot/database/histories/{str(call.from_user.id)}.json", mode='w', encoding='utf-8') as file:
        pass
    await bot.edit_message_text(text=text.TEXT_3, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=inline_kb.end_chat)
    await state.set_state(UserMessages.to_gpt)

# обрабатывает диалог с нейронкой
@router.message(UserMessages.to_gpt)
async def gpt_answer(message: Message, state: FSMContext, bot: Bot):
    print("Текст пользователя: " + message.text)
    user = await rq.search_id(message.from_user.id)
    print(user.sub_type)
    if (user.sub_type == "paid" and user.rq_made < PAID_LIMIT) or (user.sub_type == "basic" and user.rq_made < BASIC_LIMIT): # проверяет достаточно ли запросов у юзера
        if not os.path.exists(f"./bot/database/histories/{message.from_user.id}.json"):
            os.mknod(f"./bot/database/histories/{message.from_user.id}.json")
            print("файл создан")
        #создание истории json если ее нет и забирание того что там
        with open(file=f"./bot/database/histories/{str(message.from_user.id)}.json", mode='r', encoding='utf-8') as file:
            if file.readline() == "":
                history = []
            else:
                file.seek(0)
                history = json.load(file)
        typing_task = asyncio.create_task(send_typing_action(message.from_user.id, bot))
        print(f"Изначальная история: {history}")
        epoch = get_epoch()
        history.append({"role":"user", "content": message.text, "content_type":"text", "epoch":epoch})

        try:
            response = await coze_request(str(message.from_user.id), message.text, history)
            if 'role' in response and 'type' in response and 'content' in response:
                epoch = get_epoch()
                response['epoch'] = epoch
                history.append(response)
                print(f"История с ответом: {history}")
                with open(file=f"./bot/database/histories/{str(message.from_user.id)}.json", mode='w',
                          encoding='utf-8') as file:
                    json.dump(history, file, ensure_ascii=False, indent=4)
                    print("файл записан")

                await message.answer(response['content'], reply_markup=inline_kb.end_chat)
                await rq.plus_rq_made(message.from_user.id)
                await state.set_state(UserMessages.to_gpt)
            else:
                await message.answer(text.TEXT_29, reply_markup=inline_kb.end_chat)
        finally:
            typing_task.cancel()
            await typing_task

        # for i in response:
        #     history.append(i)
        # print(f"История с ответом: {history}")
        # with open(file=f"./bot/database/histories/{str(message.from_user.id)}.json", mode='w', encoding='utf-8') as file:
        #     json.dump(history, file, ensure_ascii=False, indent=4)
        #     print("файл записан")
        #
        # await message.answer(response[0]['content'], reply_markup=inline_kb.end_chat)
        # await rq.plus_rq_made(message.from_user.id)
        # await state.set_state(UserMessages.to_gpt)

    elif user.sub_type == "basic" and user.rq_made >= BASIC_LIMIT: # при бесплатной подписке предлагает купить
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text=text.INLINE_6, callback_data="back"))
        kb = (await payments_button(message.from_user.id, kb)).as_markup()
        await message.answer(text.TEXT_20, reply_markup=kb)

    elif user.sub_type == "paid" and user.rq_made>=PAID_LIMIT: # при платной говорит что лимиты закончились и все
        await message.answer(text.TEXT_21, reply_markup=inline_kb.end_chat)




# завершает чат
@router.callback_query(F.data == "end_chat")
async def back(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    with open(file=f"./bot/database/histories/{str(call.from_user.id)}.json", mode='w', encoding='utf-8') as file:
        pass
    await call.message.answer(text.TEXT_1, reply_markup=inline_kb.menu_kb)

# назад в меню
@router.callback_query(F.data == "back")
async def back(call: CallbackQuery, bot: Bot):
    await bot.edit_message_text(text=text.TEXT_1, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=inline_kb.menu_kb)

# профиль юзера
@router.callback_query(F.data == "profile")
async def back(call: CallbackQuery, bot: Bot):
    user = await rq.get_user(call.from_user.id)
    if user.sub_type == "basic":
        sub_type = "бесплатная"
        limit = BASIC_LIMIT
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text=text.INLINE_6, callback_data="back"))
        kb = (await payments_button(call.from_user.id, kb)).as_markup()
    elif user.sub_type == "paid":
        sub_type = "платная"
        limit = PAID_LIMIT
        kb = inline_kb.back_to_menu
    await bot.edit_message_text(text=f"""{call.from_user.first_name}, {text.TEXT_4}\n"""
                                     f"""ID: {call.from_user.id}\n"""
                                     f"""{text.TEXT_5} {sub_type}\n"""
                                     f"""\n"""
                                     f"""{text.TEXT_10}\n"""
                                     f"""{text.TEXT_11} {user.rq_made}/{limit} {text.TEXT_12}\n"""
                                     f"""{text.TEXT_13}""",
                                chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=kb)

# вызов кнопки оплаты подписки, не юзается так как сделано через робокассу,
# но можно сделать через внутренние возможности телеграма
@router.callback_query(F.data == "bye_sub")
async def bye_sub(call: CallbackQuery, bot: Bot):
    await bot.edit_message_text(text=text.TEXT_6, chat_id=call.message.chat.id, message_id=call.message.message_id)
    price = LabeledPrice(label=text.TEXT_7, amount=int(PRICE)*100) # цена в копейках
    await bot.send_invoice(call.message.chat.id,
                           title=text.TEXT_7,
                           description=text.TEXT_8,
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[price],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")

# проверка платежа
@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

# если платеж прошел
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, bot: Bot):
    await rq.sub_type_paid(message.from_user.id)
    await message.answer(text.TEXT_9)
    user = await rq.get_user(message.from_user.id)
    if user.sub_type == "basic":
        sub_type = "бесплатная"
        limit = BASIC_LIMIT
    elif user.sub_type == "paid":
        sub_type = "платная"
        limit = PAID_LIMIT
    await message.answer(text=f"""{message.from_user.first_name}, {text.TEXT_4}\n"""
                                     f"""ID: {message.from_user.id}\n"""
                                     f"""{text.TEXT_5} {sub_type}\n"""
                                     f"""\n"""
                                     f"""{text.TEXT_10}\n"""
                                     f"""{text.TEXT_11} {user.rq_made}/{limit} {text.TEXT_12}\n"""
                                     f"""{text.TEXT_13}""",
                                reply_markup=inline_kb.back_to_menu)