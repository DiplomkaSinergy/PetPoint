# handlers/shops.py
from aiogram import types, Router
from aiogram.filters import Command
from db.database import fetch

router = Router()

@router.message(Command("shops"))
async def show_shops(message: types.Message):
    shops = await fetch("SELECT name, address FROM shops;")
    if shops:
        reply_text = "Список магазинов:\n\n" + "\n".join([f"{shop['name']} - {shop['address']}" for shop in shops])
    else:
        reply_text = "Магазины пока отсутствуют."
    await message.answer(reply_text)

@router.message(lambda message: message.text is not None and message.text.lower() == "магазины")
async def handle_show_shops_text(message: types.Message):
    return await show_shops(message)
