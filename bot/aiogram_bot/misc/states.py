from aiogram.fsm.state import StatesGroup, State

class UserMessages(StatesGroup):
    to_gpt = State()
class OneMoreState(StatesGroup):
    something = State()

