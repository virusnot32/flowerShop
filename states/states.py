from aiogram.fsm.state import StatesGroup, State

# Определение состояний
class OrderState(StatesGroup):
    choose_flower = State()
    enter_quantity = State()
    confirm_order = State()

class AdminState(StatesGroup):
    add_flower = State()
    delete_flower = State()
    delete_user = State()
    delete_order = State()