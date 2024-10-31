from aiogram import types, F, Router
from handlers.handlers import list_directory_text

router = Router()


@router.callback_query(F.data == "load")
async def load_to_disk(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "Давайте загрузим файлы! Просто отправьте любое фото боту! \n"
    )


# Получаем содержимое папки Яндекс.Диска
@router.callback_query(F.data == "dir")
async def list_directory(callback_query: types.CallbackQuery, client, LEXICON_RU: dict):
    folder = LEXICON_RU['folder']
    try:
        files = client.listdir(f"/{folder}")
        response = f"Содержимое папки {folder}:\n"

        async for file in files:
            response += f" {file.name}\n"

        await callback_query.message.answer(response)
    except Exception as e:
        await callback_query.message.answer(f"Папки для загрузки не существует. Я создам!\n Ошибка: {str(e)}")
        await client.mkdir(f"/{folder}/")
        await callback_query.message.answer(f'Папка "{folder}" успешно создана.')
