from aiogram.dispatcher.filters.state import StatesGroup, State


class STATES(StatesGroup):
    default = State()
    entering_data = State()
    bombing = State()
    changing = State()
    blocking = State()
    notify = State()
