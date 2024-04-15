# handlers/admin.py
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.database import execute
from config import ADMIN_IDS
from states.states import CategoryState

# from keyboards.admin import get_admin_keyboard
from keyboards.admin import kb
from keyboards.common import get_main_menu_keyboard

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await message.answer("Добро пожаловать в админ-панель.",  reply_markup=keyboard)
    else:
        await message.answer("Доступ запрещен.")

@router.message(Command("add_category"))
async def cmd_add_category(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("Доступ запрещен.")
    await message.answer("Введите название категории:")
    # Используйте set_state() на объекте state, передавая туда ваше состояние
    await state.set_state(CategoryState.waiting_for_category_name)

@router.message(CategoryState.waiting_for_category_name)
async def category_name_entered(message: types.Message, state: FSMContext):
    category_name = message.text
    query = "INSERT INTO categories (name) VALUES (%s);"
    await execute(query, (category_name,))
    await message.answer(f"Категория '{category_name}' добавлена.")
    # Используйте clear() для очистки состояния
    await state.clear()
