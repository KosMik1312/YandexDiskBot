import asyncio
import logging

from aiogram import Dispatcher

import config
from db.db import create_database
from handlers import handlers
from callbacks import callbacks
from lexicon.lexicon_ru import LEXICON_RU
from main_menu.main_menu import set_main_menu, set_my_description
from middlewares.middlewares import MessageMiddleware
from aiogram.fsm.storage.memory import MemoryStorage

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


async def main():
    # Диспетчер
    dp = Dispatcher(storage=MemoryStorage())

    db_conn = await create_database()
    # Регистрируем асинхронную функцию middlewares
    dp.update.middleware(MessageMiddleware(db_conn))

    # Регистрируем асинхронные функции и роутеры в диспетчере
    dp.startup.register(set_main_menu)
    dp.startup.register(set_my_description)
    dp.include_routers(handlers.router, callbacks.router)

    # Создаём workflow_data для переменных окружения
    dp.workflow_data.update({'bot': config.bot,
                             'client': config.client,
                             'TOKEN': config.TOKEN,
                             'LEXICON_RU': LEXICON_RU,
                             'bot_url': config.bot_url})

    # Start the bot if it hasn't been started already
    await dp.start_polling(config.bot)

    # Check the validity of the token
    async with config.client:
        await config.client.check_token()


if __name__ == "__main__":
    asyncio.run(main())
