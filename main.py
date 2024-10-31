import asyncio
import logging
import os
import yadisk

from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties  # настройки редактирования бота
from aiogram.enums import ParseMode

from lexicon.lexicon_ru import LEXICON_RU
from main_menu.main_menu import set_main_menu, set_my_description
from handlers import handlers
from callbacks import callbacks

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Загружаем TOKEN
load_dotenv()


async def main():
    TOKEN = os.getenv("TOKEN")
    API_KEY = os.getenv("API_KEY")

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))  # Объект бота
    dp = Dispatcher()  # Диспетчер

    client = yadisk.AsyncClient(token=API_KEY)
    folder = LEXICON_RU['folder']

    # Регистрируем асинхронные функции и роутеры в диспетчере
    dp.startup.register(set_main_menu)
    dp.startup.register(set_my_description)
    dp.include_routers(handlers.router, callbacks.router)

    # Создаём workflow_data для переменных окружения
    dp.workflow_data.update({'bot': bot, 'client': client, 'TOKEN': TOKEN, 'LEXICON_RU': LEXICON_RU})

    # Запуск процесса поллинга новых апдейтов
    await dp.start_polling(bot)

    # Проверяет, валиден ли токен
    async with client:
        await client.check_token()

if __name__ == "__main__":
    asyncio.run(main())
