# handlers/start.py
from aiogram import types, Router, html
from aiogram.filters import Command
# from keyboards.admin import get_admin_keyboard
from keyboards.common import get_main_menu_keyboard

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    
    keyboard = types.ReplyKeyboardMarkup(keyboard=get_main_menu_keyboard())

    user_first_name = message.from_user.first_name
    welcome_text = (
        f"Привет, {html.bold(user_first_name)}! 👋\n"
        "Добро пожаловать в зоомагазин PetPoint! 🐾\n\n"
        "Я помогу тебе с выбором и покупкой товаров для твоих питомцев."
    )
    await message.answer(welcome_text, reply_markup=keyboard)
