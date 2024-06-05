from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.utils.config import ADMIN_ID


class IsAdminMiddleware(BaseMiddleware):

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
            data: Dict[str, Any]) -> Any:
        if isinstance(event, CallbackQuery):
            if event.data.startswith("admin"):
                if event.from_user.id == ADMIN_ID:
                    pass
                else:
                    return
        await handler(event, data)
