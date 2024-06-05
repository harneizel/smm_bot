from typing import Union, List

from aiogram import types, Bot
from aiogram.utils.media_group import MediaGroupBuilder


async def copy_media(
        data: Union[List[types.Message], types.Message],
        chat_id: int,
        bot: Bot,
        caption_add: str = None,
        replace_caption: bool = False
):
    """
    Копироует медиагруппы в конкретный чат с возможностью обновить или заменить текст
    :param data: Список сообщений или сообщение с которыми нужно работать
    :param chat_id: ID чата, куда нужно скопировать сообщение
    :param bot: Инстанс бота
    :param caption_add: Описание к добавлению или замене
    :param replace_caption: Заменивать ли описание (параметр caption_add) //
        False - добавить к существующему | True - Заменить на новое
    """

    async def get_media(
            data_: Union[List[types.Message], types.Message],
            caption_add_: str = None,
            replace_caption_: bool = False
    ):
        if isinstance(data_, list):
            caption = getattr(data_[0], 'html_text', '')
            if caption_add_:
                if replace_caption_:
                    caption = caption
                else:
                    caption += caption_add_
            media_group = MediaGroupBuilder(caption=caption)
            for msg in data_:
                type_msg = msg.content_type.value
                try:
                    media = getattr(msg, type_msg)[0].file_id
                except TypeError:
                    media = getattr(msg, type_msg).file_id
                media_group.add(type=type_msg, media=media, parse_mode='HTML')

            return media_group
        else:
            message = data_
            if caption_add_:
                upd = {}
                if message.content_type.value == 'text':
                    upd['text'] = (message.text or '') + caption_add_
                else:
                    upd['caption'] = (message.caption or '') + caption_add_
                message = message.model_copy(update=upd)
            return message

    data = await get_media(data, caption_add, replace_caption_=replace_caption)
    if isinstance(data, types.Message):
        return [await data.send_copy(chat_id, parse_mode='HTML')]
    else:
        return await bot.send_media_group(chat_id, data.build())
