import emoji

from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


# Хэндлер на команду /start
@router.message(Command('start'))
async def cmd_start(message: types.Message):
    # генерация клавиатуры
    builder = InlineKeyboardBuilder()
    builder.button(text=emoji.emojize(":down_arrow: Загрузить файлы"), callback_data="load")
    builder.button(text=emoji.emojize(":clockwise_vertical_arrows: Показать список файлов"), callback_data="dir")
    # сообщение
    await message.answer(
        "<b>Выберите пожалуйста действие:</b> \n"
        "/start - запуск бота\n"
        "/load - загрузить файл\n"
        "/dir - показать список файлов\n"
        "/help - что умеет этот бот\n",
        reply_markup=builder.as_markup(),
    )


# Хэндлер на команду /help
@router.message(Command("help"))
async def cmd_answer(message: types.Message, LEXICON_RU: dict):
    await message.answer(LEXICON_RU['t_help'])


# Хэндлер на команду /load
@router.message(Command("load"))
async def load_to_disk_text(message: types.Message):
    await message.answer(
        "Давайте загрузим файлы! Просто отправьте любое фото боту! \n"
    )


# Хэндлер, который получает URL файла-фото и загружает его на диск
@router.message(F.photo)
async def get_file_url(message: types.Message, bot, client, TOKEN, LEXICON_RU: dict):
    folder = LEXICON_RU['folder']
    await message.answer(f'Фото получил! Загружаю на ваш Яндекс.Диск в папку {folder}!')
    # Получаем file_id документа
    file_id = message.photo[-1]
    # Получаем информацию о файле
    file = await bot.get_file(file_id.file_id)

    # Формируем URL
    file_path = file.file_path
    url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    # Получаем имя файла для загрузки на диск
    file_name = file_path[-11:]

    #await message.answer(f"URL вашего файла: {url}")# если нужно показать URL
    await client.upload_url(f"https://api.telegram.org/file/bot{TOKEN}/{file_path}", f'disk:/{folder}/{file_name}')
    await bot.send_message(message.from_user.id, 'Фотографии загружены!')


# Хэндлер на команду /dir
@router.message(Command("dir"))
async def list_directory_text(message: types.Message, client, LEXICON_RU: dict):
    folder = LEXICON_RU['folder']
    try:
        files = client.listdir(f"/{folder}")
        response = f"Содержимое папки {folder}:\n"

        async for file in files:
            response += f" {file.name}\n"

        await message.answer(response)
    except Exception as e:
        await message.answer(f"Папки для загрузки не существует. Я создам!\n Ошибка: {str(e)}")
        await client.mkdir(f"/{folder}/")
        await message.answer(f'Папка "{folder}" успешно создана.')

