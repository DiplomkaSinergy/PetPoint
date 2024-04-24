# keyboards/admin.py
from aiogram import types

kb = [
    [types.KeyboardButton(text="Добавить категорию")],
    [types.KeyboardButton(text="Добавить товар")],
    [types.KeyboardButton(text="Добавить магазин")],
    [types.KeyboardButton(text="Удалить товар")],
    [types.KeyboardButton(text="Удалить магазин")],
    [types.KeyboardButton(text="Просмотр заказов")],
    ]

