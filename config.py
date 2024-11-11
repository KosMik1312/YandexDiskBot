import os
from aiogram import Bot, Dispatcher
import yadisk

from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties  # настройки редактирования бота
from aiogram.enums import ParseMode

# Загружаем TOKEN и API_KEY
load_dotenv()

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")
bot_url = 'https://api.telegram.org/file/bot'

# Настройки бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))  # Объект бота

# Настройки Яндекс.Диска
client = yadisk.AsyncClient(token=API_KEY)


