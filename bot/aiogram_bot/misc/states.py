from aiogram.fsm.state import StatesGroup, State

class UserMessages(StatesGroup):
    to_gpt = State()
class AdminState(StatesGroup):
    username = State()
    user_id = State()

