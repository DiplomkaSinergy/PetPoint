# states/states.py
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class ShopState(StatesGroup):
    waiting_for_shop_name = State()
    waiting_for_address = State()
    choosing_shop_for_deletion = State()

    choosing_shop = State()
    choosing_products = State()
    entering_pickup_address = State()

class OrderState(StatesGroup):
    viewing_cart = State()
    confirming_order = State()
    entering_quantity = State()
    choosing_pickup_address = State()

class BuyingProcessState(StatesGroup):
    choosing_shop = State()
    choosing_category = State()
    choosing_products = State()
    waiting_for_quantity = State()
    viewing_cart = State()
    confirming_order = State()

class ShoppingCart(StatesGroup):
    choosing_products = State()

class CategoryState(StatesGroup):
    waiting_for_category_name = State()

class ProductState(StatesGroup):
    waiting_for_product_name = State()
    waiting_for_description = State()
    waiting_for_photo = State()
    waiting_for_category = State()
    waiting_for_price = State()
    waiting_for_stock = State()
    waiting_for_shop = State()

class EditProductState(StatesGroup):
    choosing_product = State()
    choosing_attribute = State()
    entering_new_value = State() 