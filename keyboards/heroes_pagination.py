from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.dota2_heroes import DOTA2_HEROES

heroes_list_cb_data = CallbackData('pagination', "page")


def get_ikb_heroes_pagination(page: int, heroes_per_page: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)

    row = []

    if page > 1:
        row.append(InlineKeyboardButton(text='Предыдущая страница',
                                        callback_data=heroes_list_cb_data.new(page=page-1)))

    max_page = (len(DOTA2_HEROES.keys()) // heroes_per_page) + 1
    if page < max_page:
        row.append(InlineKeyboardButton(text='Следующая страница',
                                        callback_data=heroes_list_cb_data.new(page=page + 1)))

    ikb.add(*row)

    return ikb
