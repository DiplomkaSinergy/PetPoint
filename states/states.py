# states/states.py
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class CategoryState(StatesGroup):
    waiting_for_category_name = State()
