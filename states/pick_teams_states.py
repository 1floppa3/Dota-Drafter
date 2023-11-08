from aiogram.dispatcher.filters.state import StatesGroup, State


class TeamPickState(StatesGroup):
    first_team = State()
    second_team = State()
