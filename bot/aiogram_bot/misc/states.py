from aiogram.fsm.state import StatesGroup, State

class NewState(StatesGroup):
    message = State()

class OneMoreState(StatesGroup):
    something = State()

