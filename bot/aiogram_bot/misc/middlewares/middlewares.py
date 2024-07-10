from aiogram import BaseMiddleware, Bot
from aiogram.types import Update, Message
from aiogram.enums.chat_member_status import ChatMemberStatus as mbStatus
from aiogram.enums.chat_type import ChatType
from aiogram.exceptions import TelegramBadRequest
from bot.texts import *
from bot.aiogram_bot.markups.inline.menu_kb import start_inlinekeyboard
from bot.database.requests import is_user, add_user
from bot.aiogram_bot.markups.inline.menu_kb import rules_approval
from bot.utils.config import CHANNEL_ID as channel_id, LOGS_ID as logs_id

# если юзер не подписан на канал бот не будет с ним работать
class SubsriptionMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, channel_id: int):
        self.bot = bot
        self.channel_id = channel_id
        super().__init__()

    async def __call__(self, handler, event: Update, data: dict):
        print(event)
        if event.message and event.message.chat.type=="private":
            user_id = event.message.from_user.id
            print(f"Юзер ID: {user_id}")
            member = await self.bot.get_chat_member(channel_id, user_id)
            print(member.status)

            if await is_user(user_id) == "not_user":
                await add_user(user_id, event.message.from_user.first_name, event.message.from_user.username)
                await self.bot.send_message(chat_id=logs_id,
                                       text=f"""#пользователь{user_id}\nid:`{user_id}`\n{TEXT_31}""")
                await event.message.answer(text=TEXT_27, reply_markup=rules_approval)
            elif member.status in [mbStatus.MEMBER, mbStatus.CREATOR, mbStatus.ADMINISTRATOR]:
                return await handler(event, data)
            else:
                await event.message.answer(text=START_TEXT, reply_markup=start_inlinekeyboard)
            #except TelegramBadRequest:
                #await event.message.answer(TEXT_14)
                #print(TelegramBadRequest)
        elif event.pre_checkout_query:
            user_id = event.pre_checkout_query.from_user.id
            member = await self.bot.get_chat_member(self.channel_id, user_id)
            print(member)
            if member.status in [mbStatus.MEMBER, mbStatus.CREATOR, mbStatus.ADMINISTRATOR]:
                return await handler(event, data)
            else:
                await event.message.answer(text=START_TEXT, reply_markup=start_inlinekeyboard)
        elif event.callback_query and event.callback_query.message.chat.type == "private":
            user_id = event.callback_query.from_user.id
            #try:
            member = await self.bot.get_chat_member(self.channel_id, user_id)
            print(member)
            if member.status in [mbStatus.MEMBER, mbStatus.CREATOR, mbStatus.ADMINISTRATOR]:
                return await handler(event, data)
            elif event.callback_query.data=="agree":
                return await handler(event, data)
            else:
                await event.callback_query.message.answer(text=START_TEXT, reply_markup=start_inlinekeyboard)
            #except TelegramBadRequest:
                #await event.callback_query.message.answer(text=TEXT_14)


class UnsubscribeMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        if event.chat_member:
            print(event.chat_member.new_chat_member)
        else:
            return await handler(event, data)

