from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.utils.config import ADMIN_IDS


class IsAdmin(BaseFilter):
    def __int__(self, ADMIN_IDS) -> None:
        self.ADMIN_IDS = ADMIN_IDS
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.ADMIN_IDS
