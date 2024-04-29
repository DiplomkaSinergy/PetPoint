# handlers/products.py
from aiogram import types, Router
from aiogram.filters import Command
from db.database import fetch

router = Router()

@router.message(Command("view_products"))
async def view_products(message: types.Message):
    # Измененный SQL запрос с JOIN для получения названия категории
    view_prodits_querry = """
    SELECT p.id, p.name, p.description, p.price, p.stock, c.name AS category_name
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.id;
    """
    products = await fetch(view_prodits_querry)
    if not products:
        await message.answer("В настоящее время нет доступных товаров.")
    else:
        products_text = []
        for product in products:
            products_text.append(
                "-------------------------\n"
                f"ID: {product['id']}\n"
                f"Название: {product['name']}\n"
                f"Описание: {product['description']}\n"
                f"Категория: {product['category_name']}\n"
                f"Цена: {product['price']} руб.\n"
                f"На складе: {product['stock']} шт.\n"
            )
        await message.answer("\n".join(products_text))

# @router.message(lambda message: message.text.lower() == "посмотреть товары")
# async def handle_get_products_text(message: types.Message):
#     return await view_products(message)