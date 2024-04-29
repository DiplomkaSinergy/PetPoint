from aiogram import types, Router
from aiogram.filters import Command
from db.database import fetch

router = Router()

# Мои заказы (заказы пользователя)
@router.message(Command("my_orders"))
async def show_my_orders(message: types.Message):
    user_id = message.from_user.id
    orders = await fetch("SELECT id, status, total_price, pickup_address FROM orders WHERE user_id = %s;", (user_id,))

    if orders:
        reply_text = "Ваши заказы:\n\n"
        for order in orders:
            reply_text += f"Заказ №{order['id']}\nСтатус: {order['status']}\nСумма заказа: {order['total_price']} руб.\nАдрес для самовывоза: {order['pickup_address']}\n\n"
    else:
        reply_text = "У вас пока нет заказов."

    await message.answer(reply_text)


@router.message(lambda message: message.text is not None and message.text.lower() == "мои заказы")
async def handle_show_my_orders_text(message: types.Message):
    return await show_my_orders(message)
