# keyboards/cancel.py
from aiogram import types

def get_cancel_keyboard():
    kb = [
        [types.KeyboardButton(text="Отмена")],
    ]
    return kb
