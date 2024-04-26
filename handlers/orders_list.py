# handlers/orders_list.py
from aiogram import types, Router
from aiogram.filters import Command
from db.database import fetch
from config import ADMIN_IDS

router = Router()

@router.message(Command("list_orders"))
async def list_orders(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Доступ запрещен.")
        return

    orders = await fetch("SELECT id, user_id, status, total_price, pickup_address FROM orders;")
    if orders:
        reply_text = "Список заказов:\n"
        for order in orders:
            reply_text += f"ID заказа: {order['id']}\nID пользователя: {order['user_id']}\nСтатус: {order['status']}\nСумма: {order['total_price']} руб.\nАдрес для самовывоза: {order['pickup_address']}\n\n"
    else:
        reply_text = "Заказы отсутствуют."
    
    await message.answer(reply_text)

@router.message(lambda message: message.text is not None and message.text.lower() == "список заказов")
async def handle_show_my_orders_text(message: types.Message):
    return await list_orders(message)
