from aiogram.dispatcher.filters.state import StatesGroup, State


class BotMailingState(StatesGroup):
    text = State()
    state = State()
    photo = State()
