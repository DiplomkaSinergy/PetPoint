# handlers/categories.py
from aiogram import types, Router
from aiogram.filters import Command
from db.database import fetch

# Создаем объект Router для этого файла
router = Router()

# Регистрируем обработчик для команды "categories"
@router.message(Command("categories"))
async def show_categories(message: types.Message):
    categories = await fetch("SELECT name FROM categories;")
    if categories:
        reply_text = "Выберите категорию:\n\n" + "\n".join([f"- {category['name']}" for category in categories])
    else:
        reply_text = "Категории пока отсутствуют."
    await message.answer(reply_text)
