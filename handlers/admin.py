from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.database import execute, fetch
from config import ADMIN_IDS
from states.states import CategoryState, ShopState, ProductState, EditProductState

router = Router()

# Панель администратора
@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        admin_menu = [
            [types.KeyboardButton(text="Добавить магазин")],
            [types.KeyboardButton(text="Добавить категорию")],
            [types.KeyboardButton(text="Добавить товар")],
            [types.KeyboardButton(text="Редактировать товар")],
            [types.KeyboardButton(text="Удалить товар")],
            [types.KeyboardButton(text="Удалить магазин")],
            [types.KeyboardButton(text="Просмотр заказов")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=admin_menu, resize_keyboard=True, one_time_keyboard=True)
        await message.answer("Добро пожаловать в админ-панель.", reply_markup=keyboard)
    else:
        await message.answer("Доступ запрещен.")

# Добавление магазина
@router.message(Command("add_shop"))
async def cmd_add_shop(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Доступ запрещен.")
    else:
        await message.answer("Введите название магазина:")
        await state.set_state(ShopState.waiting_for_shop_name)

@router.message(ShopState.waiting_for_shop_name)
async def shop_name_entered(message: types.Message, state: FSMContext):
    await state.update_data(shop_name=message.text)
    await message.answer("Введите адрес магазина:")
    await state.set_state(ShopState.waiting_for_address)

@router.message(ShopState.waiting_for_address)
async def address_entered(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await execute("INSERT INTO shops (name, address) VALUES (%s, %s);", (data['shop_name'], message.text))
    await message.answer(f"Магазин '{data['shop_name']}' добавлен по адресу '{message.text}'.")
    await state.clear()

# Добавление категории товара
@router.message(Command("add_category"))
async def cmd_add_category(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Доступ запрещен.")
    else:
        await message.answer("Введите название категории:")
        await state.set_state(CategoryState.waiting_for_category_name)

@router.message(CategoryState.waiting_for_category_name)
async def category_name_entered(message: types.Message, state: FSMContext):
    await execute("INSERT INTO categories (name) VALUES (%s);", (message.text,))
    await message.answer(f"Категория '{message.text}' добавлена.")
    await state.clear()

# Добавление товара
@router.message(Command("add_product"))
async def cmd_add_product(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Доступ запрещен.")
    else:
        await message.answer("Введите название товара:")
        await state.set_state(ProductState.waiting_for_product_name)

@router.message(ProductState.waiting_for_product_name)
async def product_name_entered(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара:")
    await state.set_state(ProductState.waiting_for_description)

@router.message(ProductState.waiting_for_description)
async def product_description_entered(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    categories = await fetch("SELECT id, name FROM categories ORDER BY id;")
    if categories:
        category_list = '\n'.join([f"{category['id']} - {category['name']}" for category in categories])
        await message.answer(f"Выберите категорию по ID:\n{category_list}")
        await state.set_state(ProductState.waiting_for_category)
    else:
        await message.answer("Категории отсутствуют. Пожалуйста, добавьте категорию.")
        await state.clear()

@router.message(ProductState.waiting_for_category)
async def category_selected(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        category_id = int(message.text)
        category = await fetch(f"SELECT id FROM categories WHERE id = {category_id};")
        if category:
            await state.update_data(category_id=category_id)
            await message.answer("Введите цену товара:")
            await state.set_state(ProductState.waiting_for_price)
        else:
            await message.answer("Недействительный ID категории. Пожалуйста, введите действительный ID.")
    else:
        await message.reply("Пожалуйста, введите действительный числовой ID категории.")

@router.message(ProductState.waiting_for_price)
async def product_price_entered(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Введите количество товара на складе:")
    await state.set_state(ProductState.waiting_for_stock)

@router.message(ProductState.waiting_for_stock)
async def product_stock_entered(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply("Пожалуйста, введите действительное числовое значение для количества товара.")
        return
    await state.update_data(stock=int(message.text))
    data = await state.get_data()
    try:
        await execute("INSERT INTO products (name, description, category_id, price, stock) VALUES (%s, %s, %s, %s, %s);",
                      (data['name'], data['description'], int(data['category_id']), float(data['price']), int(data['stock'])))
        await message.answer(f"Товар '{data['name']}' успешно добавлен.")
    except Exception as e:
        await message.answer(f"Не удалось добавить товар: {str(e)}")
    finally:
        await state.clear()

# Начало процесса редактирования товара
@router.message(Command("edit_product"))
async def start_edit_product(message: types.Message, state: FSMContext):
    products = await fetch("SELECT id, name FROM products;")
    if products:
        product_list = "\n".join([f"{product['id']} - {product['name']}" for product in products])
        await message.answer(f"Выберите товар для редактирования, отправив его ID:\n{product_list}")
        await state.set_state(EditProductState.choosing_product)
    else:
        await message.answer("Товары отсутствуют.")

@router.message(EditProductState.choosing_product)
async def choose_product(message: types.Message, state: FSMContext):
    product_id = message.text.strip()
    if product_id.isdigit():
        product = await fetch(f"SELECT * FROM products WHERE id = {product_id};")
        if product:
            await state.update_data(product_id=product_id)
            options = "Введите номер параметра для редактирования:\n1 - Название\n2 - Описание\n3 - Цена\n4 - Количество"
            await message.answer(options)
            await state.set_state(EditProductState.choosing_attribute)
        else:
            await message.answer("Товар не найден. Пожалуйста, введите корректный ID.")
    else:
        await message.answer("Пожалуйста, введите число.")

@router.message(EditProductState.choosing_attribute)
async def choose_attribute(message: types.Message, state: FSMContext):
    choice = message.text.strip()
    valid_choices = {"1": "name", "2": "description", "3": "price", "4": "stock"}
    if choice in valid_choices:
        await state.update_data(attribute=valid_choices[choice])
        await message.answer("Введите новое значение:")
        await state.set_state(EditProductState.entering_new_value)
    else:
        await message.answer("Неверный выбор, пожалуйста, выберите один из доступных параметров.")

@router.message(EditProductState.entering_new_value)
async def update_product(message: types.Message, state: FSMContext):
    new_value = message.text.strip()
    data = await state.get_data()
    product_id = data['product_id']
    attribute = data['attribute']
    await execute(f"UPDATE products SET {attribute} = %s WHERE id = %s;", (new_value, product_id))
    await message.answer(f"Товар обновлён: {attribute} теперь '{new_value}'.")
    await state.clear()

@router.message(lambda message: message.text.lower() == "добавить магазин")
async def handle_add_shop_text(message: types.Message, state: FSMContext):
    return await cmd_add_shop(message, state)

@router.message(lambda message: message.text.lower() == "добавить категорию")
async def handle_add_category_text(message: types.Message, state: FSMContext):
    return await cmd_add_category(message, state)

@router.message(lambda message: message.text.lower() == "добавить товар")
async def handle_add_product_text(message: types.Message, state: FSMContext):
    return await cmd_add_product(message, state)

@router.message(lambda message: message.text.lower() == "редактировать товар")
async def handle_edit_product_text(message: types.Message, state: FSMContext):
    return await start_edit_product(message, state)

@router.message(lambda message: message.text.lower() == "отмена")
async def cancel_action(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=ReplyKeyboardRemove())
