import datetime
from typing import Dict, Any, Callable, Awaitable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, TelegramObject, CallbackQuery


class AntiFloodMiddleware(BaseMiddleware):
    time_updates: Dict[int, datetime.datetime] = {}
    message_counts: Dict[int, int] = {}
    timedelta_limiter: datetime.timedelta = datetime.timedelta(seconds=1)
    max_messages_per_second: int = 2

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id

            # Обновляем количество сообщений от пользователя в текущую секунду
            if user_id in self.time_updates.keys():
                current_time = datetime.datetime.now()
                if (current_time - self.time_updates[user_id]) > self.timedelta_limiter:
                    # Если прошла секунда, обнуляем счетчик и обновляем метку времени
                    self.message_counts[user_id] = 1
                    self.time_updates[user_id] = current_time
                else:
                    # Если еще не прошла секунда, увеличиваем счетчик
                    self.message_counts[user_id] += 1

                # Если количество сообщений превышает лимит, игнорируем событие
                if self.message_counts[user_id] > self.max_messages_per_second:
                    return None
            else:
                # Если это первое сообщение в текущей секунде, инициализируем счетчик и метку времени
                self.message_counts[user_id] = 1
                self.time_updates[user_id] = datetime.datetime.now()

            # Обновляем данные в базе данных только если человек прошел антифлуд
            # Передача данных в другой миддлваре
            data["update_db"] = True
            return await handler(event, data)
