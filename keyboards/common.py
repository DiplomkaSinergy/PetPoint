# keyboards/common.py
from aiogram import types

def get_main_menu_keyboard():
    kb = [
        [types.KeyboardButton(text="Посмотреть категории")],
        [types.KeyboardButton(text="Посмотреть товары")],
        [types.KeyboardButton(text="Мои заказы")],
        [types.KeyboardButton(text="Магазины")],
    ]
    return kb
