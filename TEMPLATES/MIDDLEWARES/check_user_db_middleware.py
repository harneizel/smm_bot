from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

# from bot.database.users import get_user, add_user, update_user


class DBMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if hasattr(event, 'from_user'):
            user = await add_user(
                user_id=event.from_user.id,
                name=event.from_user.first_name,
                username=event.from_user.username,
            )

            if user.name != event.from_user.first_name or user.username != event.from_user.username:
                await update_user(
                    user_id=event.from_user.id,
                    name=event.from_user.first_name,
                    username=event.from_user.username,
                )
        return await handler(event, data)
