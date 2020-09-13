from aiogram.dispatcher.filters.state import StatesGroup, State


class STATES(StatesGroup):
    default = State()
    bombing = State()
    changing = State()
    blocking = State()
