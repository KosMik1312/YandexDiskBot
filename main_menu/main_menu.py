from aiogram import Bot
from aiogram.types import BotCommand  # иморт для стартового меню

# Создаем асинхронную функцию стартового меню
async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/load", description="Загрузка"),
        BotCommand(command="/dir", description="Показать список файлов"),
        BotCommand(command="/help", description="Справка по работе бота"),
    ]
    await bot.set_my_commands(main_menu_commands)


# Приветствие перед Start
async def set_my_description(bot: Bot):
    main_description = "Это бот умеет загружать файлы на Яндекс.Диск"
    await bot.set_my_description(main_description)