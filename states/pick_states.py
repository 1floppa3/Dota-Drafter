from aiogram.dispatcher.filters.state import StatesGroup, State


class WrongHeroState(StatesGroup):
    user_input = State()
    wrong_name = State()
    new_name = State()


class WaitForHeroesState(StatesGroup):
    heroes = State()
