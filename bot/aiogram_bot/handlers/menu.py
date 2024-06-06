import json
import os
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.database import requests as rq
from bot.utils.config import CHANNEL_ID, PAYMENTS_TOKEN, PRICE, BASIC_LIMIT, PAID_LIMIT
import bot.aiogram_bot.markups.inline.menu_kb as inline_kb
import bot.texts as text
from bot.aiogram_bot.misc.states import *
from bot.utils.api_requests import *
from bot.database import histories

router = Router()


@router.message(F.text == "/start")
async def start_btn(message: Message, bot: Bot):
    await rq.add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer(text.TEXT_1, reply_markup=inline_kb.menu_kb)

@router.callback_query(F.data == "check_sub")
async def check_sub(call: CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer(text.TEXT_1, reply_markup=inline_kb.menu_kb)

@router.callback_query(F.data == "dialogue")
async def dialogue(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text=text.TEXT_3, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=inline_kb.back)
    await state.set_state(UserMessages.to_gpt)

# обрабатывает диалог с нейронкой
@router.message(UserMessages.to_gpt)
async def gpt_answer(message: Message, state: FSMContext):
    print("Текст пользователя: " + message.text)
    #user = await rq.search_id(message.from_user.id)
    if not os.path.exists(f"./bot/database/histories/{message.from_user.id}.json"):
        os.mknod(f"./bot/database/histories/{message.from_user.id}.json")
        print("файл создан")

    with open(file=f"./bot/database/histories/{str(message.from_user.id)}.json", mode='r', encoding='utf-8') as file:
        if file.readline() == "":
            history = []
        else:
            file.seek(0)
            history = json.load(file)

    print(f"Изначальная история: {history}")

    history.append({"role":"user", "content": message.text, "content_type":"text"})
    #response = coze_request(message.from_user.id, message.text, history)
    response = {"messages": [{"role": "assistant", "type": "verbose",
                              "content": "{\"msg_type\":\"time_capsule_recall\",\"data\":\"{\\\"wraped_text\\\":\\\"\\\",\\\"origin_search_results\\\":\\\"[]\\\"}\",\"from_module\":null,\"from_unit\":null}",
                              "content_type": "text"}, {"role": "assistant", "type": "answer",
                                                        "content": "Окей Тони, смотри как мы можем это сделать. \n\nДля понимания последствий столкновения метеорита с Землей, необходимо учитывать несколько факторов: размер метеорита, его скорость, угол входа в атмосферу, а также плотность и состав метеорита. Вот несколько возможных последствий:\n\n1. **Мелкие метеориты** (до нескольких метров в диаметре):\n   - Такие метеориты обычно сгорают в атмосфере и не достигают поверхности Земли.\n   - В процессе горения они могут создать светящееся явление, известное как \"падающая звезда\" или болид (если метеорит достаточно крупный).\n\n2. **Средние метеориты** (от нескольких метров до десятков метров в диаметре):\n   - Эти метеориты могут частично сгореть в атмосфере и, если все-таки долетят до поверхности, создать кратер.\n   - Могут вызвать локальные разрушения, пожары и воздушные взрывы. \n\n3. **Крупные метеориты** (десятки метров и больше):\n   - Могут вызвать катастрофические изменения, такие как разрушение больших территорий.\n   - Создадут огромные кратеры и вызовут глобальные разрушения, такие как землетрясения, цунами и даже изменение климата вследствие выброса пыли и паров в стратосферу.\n   - Известный пример - Чиксулубский кратер, который, по мнению ученых, вызвал массовое вымирание динозавров около 66 миллионов лет назад.\n\n4. **Сверхкрупные метеориты** (более километра в диаметре):\n   - Эти объекты представляют глобальную угрозу для жизни на Земле. Могут вызвать массовое вымирание видов.\n   - Вызовут долгосрочные изменения климата, такие как \"импактная зима\", в течение которой солнечный свет будет блокирован облаком пыли и золы.\n   - Энергия их удара будет равна или превышать энергию всех ядерных арсеналов Земли.\n\nВот краткая инструкция о том, что может произойти при падении метеорита различных размеров и масс. Если тебе нужно больше информации или конкретные примеры, дай знать!",
                                                        "content_type": "text"},
                             {"role": "assistant", "type": "verbose",
                              "content": "{\"msg_type\":\"generate_answer_finish\",\"data\":\"\",\"from_module\":null,\"from_unit\":null}",
                              "content_type": "text"}], "conversation_id": "123", "code": 0, "msg": "success"}
    for i in response["messages"]:
        history.append(i)
    print(f"История с ответом: {history}")
    with open(file=f"./bot/database/histories/{str(message.from_user.id)}.json", mode='w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

    #await rq.set_history(message.from_user.id, history_string)
    await message.answer(response['messages'][1]['content'], reply_markup=inline_kb.end_chat)
    await state.set_state(UserMessages.to_gpt)
    file.close()
    #response = requests.post(url=url, headers=headers, data=json.dumps(data)).text
    #resp_text = json.loads(response)
    #return str(resp_text['messages'][1]['content']).replace('\n\n', '\n')

# завершает чат
@router.callback_query(F.data == "end_chat")
async def back(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await call.message.answer(text.TEXT_1, reply_markup=inline_kb.menu_kb)


@router.callback_query(F.data == "back")
async def back(call: CallbackQuery, bot: Bot):
    await bot.edit_message_text(text=text.TEXT_1, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=inline_kb.menu_kb)


@router.callback_query(F.data == "profile")
async def back(call: CallbackQuery, bot: Bot):
    user = await rq.get_user(call.from_user.id)
    if user.sub_type == "basic":
        sub_type = "бесплатная"
        limit = BASIC_LIMIT
    elif user.sub_type == "paid":
        sub_type = "платная"
        limit = PAID_LIMIT
    await bot.edit_message_text(text=f"""{call.from_user.first_name}, {text.TEXT_4}\n"""
                                     f"""ID: {call.from_user.id}\n"""
                                     f"""{text.TEXT_5} {sub_type}\n"""
                                     f"""\n"""
                                     f"""{text.TEXT_10}\n"""
                                     f"""{text.TEXT_11} {user.rq_made}/{limit} {text.TEXT_12}\n"""
                                     f"""{text.TEXT_13}""",
                                chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=inline_kb.profile)

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
                                reply_markup=inline_kb.profile)