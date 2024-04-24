# states/states.py
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class ShopState(StatesGroup):
    waiting_for_shop_name = State()
    waiting_for_address = State()

class CategoryState(StatesGroup):
    waiting_for_category_name = State()

class ProductState(StatesGroup):
    waiting_for_product_name = State()
    waiting_for_description = State()
    waiting_for_photo = State()
    waiting_for_category = State()
    waiting_for_price = State()
    waiting_for_stock = State()

class EditProductState(StatesGroup):
    choosing_product = State()
    choosing_attribute = State()
    entering_new_value = State() 