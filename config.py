import os
from aiogram import Bot, Dispatcher
import yadisk

from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties  # настройки редактирования бота
from aiogram.enums import ParseMode
# Импортировать для работы с PythonAnyWhere
# from aiogram.client.session.aiohttp import AiohttpSession

# Загружаем TOKEN и API_KEY
load_dotenv()

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")
bot_url = 'https://api.telegram.org/file/bot'

# Подключить сессию для работы PythonАnyWhere
# session = AiohttpSession(proxy='http://proxy.server:3128')  # в proxy указан прокси сервер pythonanywhere, он нужен для подключения

# Настройки бота / для работы с PythonAnyWhere нужно добавить session=session
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))  # Объект бота

# Настройки Яндекс.Диска
client = yadisk.AsyncClient(token=API_KEY)
