# states/shop_state.py

class ShopState(StatesGroup):
    waiting_for_shop_name = State()
    waiting_for_address = State()

@router.message(Command("add_shop"))
async def cmd_add_shop(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("Доступ запрещен.")
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
    shop_name = data['shop_name']
    address = message.text
    query = "INSERT INTO shops (name, address) VALUES (%s, %s);"
    await execute(query, (shop_name, address))
    await message.answer(f"Магазин '{shop_name}' добавлен по адресу '{address}'.")
    await state.clear()
