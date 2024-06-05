from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.utils.config import ADMIN_IDS
admin_ids = [6419408258]

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in admin_ids
