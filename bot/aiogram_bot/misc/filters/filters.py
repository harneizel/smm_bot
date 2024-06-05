from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.utils.config import ADMIN_IDS


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            return message.from_user.id in ADMIN_IDS
        except:
            return False
