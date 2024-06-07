from aiogram import BaseMiddleware, Bot
from aiogram.types import Update, ChatMemberUpdated, ChatMember
from aiogram.enums.chat_member_status import ChatMemberStatus as mbStatus
from aiogram.exceptions import TelegramBadRequest
from bot.texts import *
from bot.aiogram_bot.markups.inline.menu_kb import start_inlinekeyboard

# если юзер не подписан на канал бот не будет с ним работать
class SubsriptionMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, channel_id: int):
        self.bot = bot
        self.channel_id = channel_id
        super().__init__()

    async def __call__(self, handler, event: Update, data: dict):
        print(event)
        if event.message:
            user_id = event.message.from_user.id
            try:
                member = await self.bot.get_chat_member(self.channel_id, user_id)
                print(member)
                if member.status in [mbStatus.MEMBER, mbStatus.CREATOR, mbStatus.ADMINISTRATOR]:
                    return await handler(event, data)
                else:
                    await event.message.answer(text=START_TEXT, reply_markup=start_inlinekeyboard)
            except TelegramBadRequest:
                await event.message.answer(TEXT_14)
        elif event.pre_checkout_query:
            user_id = event.pre_checkout_query.from_user.id
            try:
                member = await self.bot.get_chat_member(self.channel_id, user_id)
                print(member)
                if member.status in [mbStatus.MEMBER, mbStatus.CREATOR, mbStatus.ADMINISTRATOR]:
                    return await handler(event, data)
                else:
                    await event.message.answer(text=START_TEXT, reply_markup=start_inlinekeyboard)
            except TelegramBadRequest:
                await event.message.answer(TEXT_14)
        elif event.callback_query.data=="check_sub":
            user_id = event.callback_query.from_user.id
            try:
                member = await self.bot.get_chat_member(self.channel_id, user_id)
                print(member)
                if member.status in [mbStatus.MEMBER, mbStatus.CREATOR, mbStatus.ADMINISTRATOR]:
                    return await handler(event, data)
                else:
                    await event.message.answer(text=TEXT_15)
            except TelegramBadRequest:
                await event.message.answer(TEXT_14)
        elif event.callback_query:
            user_id = event.callback_query.from_user.id
            try:
                member = await self.bot.get_chat_member(self.channel_id, user_id)
                print(member)
                if member.status in [mbStatus.MEMBER, mbStatus.CREATOR, mbStatus.ADMINISTRATOR]:
                    return await handler(event, data)
                else:
                    await event.callback_query.message.answer(text=START_TEXT, reply_markup=start_inlinekeyboard)
            except TelegramBadRequest:
                await event.message.answer(TEXT_14)
        else:
            return await handler(event, data)


class UnsubscribeMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        if event.chat_member:
            print(event.chat_member.new_chat_member)
        else:
            return await handler(event, data)