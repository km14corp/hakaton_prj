from aiogram.dispatcher.filters.state import StatesGroup, State


class info(StatesGroup):
    name = State()
    date = State()
    time = State()
    cort = State()
    coach = State()
    inventory = State()
    receipt = State()
    tools = State()
    choose = State()
    choose_2 = State()