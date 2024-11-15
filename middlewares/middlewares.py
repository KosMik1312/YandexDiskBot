import asyncio
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


# функция отслеживает все сообщения пользователя и записывает их в базу данных
class MessageMiddleware(BaseMiddleware):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # ...
        if event.message and event.message.text is not None and event.message.text.startswith('/'):
            user_id = event.message.from_user.id
            text = event.message.text
            try:
                async with self.db_conn.cursor() as cursor:
                    await cursor.execute('INSERT INTO telegram_commands (user_id, command) VALUES (?, ?)',
                                         (user_id, text))
                    await self.db_conn.commit()
            except asyncio.exceptions.CancelledError as e:
                print(f"Задача была отменена: {e}")
            except Exception as e:
                print(f"Ошибка: {e}")

        result = await handler(event, data)
        return result
