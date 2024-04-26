from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from db.database import execute, fetch
from states.states import BuyingProcessState, OrderState
from config import PAYMENT_TOKEN

router = Router()

@router.message(Command("start_shopping"))
async def start_shopping(message: types.Message, state: FSMContext):
    shops = await fetch("SELECT id, name FROM shops;")
    if shops:
        shop_list = "\n".join([f"{shop['id']} - {shop['name']}" for shop in shops])
        await message.answer(f"Выберите магазин из списка, отправив его ID:\n{shop_list}")
        await state.set_state(BuyingProcessState.choosing_shop)
    else:
        await message.answer("Магазины отсутствуют.")

@router.message(BuyingProcessState.choosing_shop)
async def choose_shop(message: types.Message, state: FSMContext):
    shop_id = message.text.strip()
    if shop_id.isdigit():
        shop = await fetch(f"SELECT * FROM shops WHERE id = {shop_id};")
        if shop:
            await state.update_data(shop_id=shop_id)
            products = await fetch(f"SELECT id, name, stock FROM products WHERE shop_id = {shop_id};")
            if products:
                product_list = "\n".join([f"{product['id']} - {product['name']} (На складе: {product['stock']})" for product in products])
                await message.answer(f"Выберите товары, отправив их ID:\n{product_list}")
                await state.set_state(BuyingProcessState.choosing_products)
            else:
                await message.answer("Товары в этом магазине отсутствуют.")
        else:
            await message.answer("Магазин не найден. Пожалуйста, введите корректный ID.")
    else:
        await message.answer("Пожалуйста, введите число.")

@router.message(BuyingProcessState.choosing_products)
async def choose_product(message: types.Message, state: FSMContext):
    product_id = message.text.strip()
    if product_id.isdigit():
        product = await fetch(f"SELECT * FROM products WHERE id = {product_id};")
        if product:
            product = product[0]
            await state.update_data(chosen_product_id=product_id)
            await message.answer(f"Введите количество для '{product['name']}' (Доступно: {product['stock']}):")
            await state.set_state(OrderState.entering_quantity)
        else:
            await message.answer("Товар не найден. Пожалуйста, введите корректный ID.")
    else:
        await message.answer("Пожалуйста, введите число.")

@router.message(OrderState.entering_quantity)
async def enter_quantity(message: types.Message, state: FSMContext):
    if message.text.lower() == '/cart':
        await view_cart(message, state)
        await state.set_state(BuyingProcessState.choosing_products)
        return
    elif message.text.lower() == '/make_order':
        await make_order(message, state)
        return

    quantity = message.text.strip()
    if quantity.isdigit() and int(quantity) > 0:
        data = await state.get_data()
        product_id = data['chosen_product_id']
        product = await fetch(f"SELECT * FROM products WHERE id = {product_id};")
        if product:
            product = product[0]
            if int(quantity) <= product['stock']:
                cart = data.get('cart', {})
                cart[product_id] = {'name': product['name'], 'quantity': int(quantity), 'price': product['price']}
                await state.update_data(cart=cart)
                await message.answer(f"{product['name']} - {quantity} шт. добавлено в корзину.")
                await message.answer("Введите ID другого товара для добавления или введите /cart для просмотра корзины или /make_order для оформления заказа.")
            else:
                await message.answer(f"К сожалению, на складе только {product['stock']} шт. Пожалуйста, введите меньшее количество.")
        else:
            await message.answer("Произошла ошибка при получении информации о товаре.")
    else:
        await message.answer("Пожалуйста, введите корректное количество.")

@router.message(Command("cart"))
async def view_cart(message: types.Message, state: FSMContext):
    cart = (await state.get_data()).get('cart', {})
    if not cart:
        await message.answer("Ваша корзина пуста.")
        return
    
    response = []
    total_cost = 0
    for product_id, item in cart.items():
        total_cost += item['price'] * item['quantity']
        response.append(f"{item['name']} - {item['quantity']} шт. по {item['price']} руб. каждый")
    
    await message.answer("\n".join(response) + f"\nОбщая стоимость: {total_cost} руб.")
    
    # После просмотра корзины переводим пользователя обратно в состояние выбора продуктов или оформления заказа
    await state.set_state(BuyingProcessState.choosing_products)


@router.message(Command("make_order"))
async def make_order(message: types.Message, state: FSMContext):
    cart = (await state.get_data()).get('cart', {})
    if not cart:
        await message.answer("Ваша корзина пуста.")
        return

    # Получаем список доступных адресов магазинов
    shops = await fetch("SELECT id, name, address FROM shops;")
    if not shops:
        await message.answer("Извините, не удалось получить список магазинов.")
        return
    
    # Формируем список адресов для выбора
    shop_list = "\n".join([f"{shop['id']} - {shop['name']}: {shop['address']}" for shop in shops])
    await message.answer(f"Пожалуйста, выберите адрес для самовывоза:\n{shop_list}")
    await state.update_data(shop_list=shops)  # Сохраняем список магазинов в состояние
    await state.set_state(OrderState.choosing_pickup_address)  # Переходим в состояние выбора адреса

@router.message(OrderState.choosing_pickup_address)
async def choose_pickup_address(message: types.Message, state: FSMContext):
    shop_id = message.text.strip()
    if shop_id.isdigit():
        shops = (await state.get_data()).get('shop_list', [])
        selected_shop = next((shop for shop in shops if str(shop['id']) == shop_id), None)
        if selected_shop:
            # Сохраняем выбранный адрес
            await state.update_data(pickup_address=selected_shop['address'])

            # Продолжаем с оформлением заказа
            cart = (await state.get_data()).get('cart', {})
            total_cost = sum(item['price'] * item['quantity'] for item in cart.values())
            prices = [types.LabeledPrice(label="Total", amount=int(total_cost * 100))]  # сумма в копейках

            await message.bot.send_invoice(
                chat_id=message.chat.id,
                title="Заказ",
                description=f"Общая сумма покупки для самовывоза - {selected_shop['address']}",
                provider_token=PAYMENT_TOKEN,
                currency="RUB",
                prices=prices,
                payload="Unique",
                start_parameter="create_invoice",
                photo_url="https://6kcmxu3d7l.a.trbcdn.net/s3/petshop-ru-static/644051929ba0ce70af6a02c8b6403c406747bbb6.png",
                photo_size=512,
                photo_width=512,
                photo_height=512,
                need_name=True,
                need_phone_number=True,
                need_email=True,
                need_shipping_address=False,  # Так как уже выбран адрес
                is_flexible=False  # Нет изменения стоимости доставки, так как это самовывоз
            )
            await state.set_data({'cart': {}})  # Очищаем корзину после отправки инвойса
        else:
            await message.answer("Пожалуйста, выберите корректный ID магазина.")
    else:
        await message.answer("Пожалуйста, введите число.")

@router.pre_checkout_query()
async def checkout_query_handler(query: types.PreCheckoutQuery):
    await query.bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    await message.answer(f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
    await message.answer("Спасибо за ваш заказ!")
    await state.reset_state()
