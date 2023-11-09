from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

hero_skills_cb_data = CallbackData('hero_skills', "url_name")
hero_talents_cb_data = CallbackData('hero_talents', "url_name")
hero_counters_cb_data = CallbackData('hero_counters', "url_name")
hero_back_to_heroes_cb_data = CallbackData('hero_back_to_heroes', "url_name")
hero_skills_pagination_cb_data = CallbackData('skills_pagination', "url_name", "skill_num")


def get_ikb_hero_data(url_name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text='Навыки', callback_data=hero_skills_cb_data.new(url_name=url_name)),
        InlineKeyboardButton(text='Таланты', callback_data=hero_talents_cb_data.new(url_name=url_name)),
    ).add(
        InlineKeyboardButton(text='Хорош/плох против...', callback_data=hero_counters_cb_data.new(url_name=url_name))
    ).add(
        InlineKeyboardButton(text='◀️ К списку героев',
                             callback_data=hero_back_to_heroes_cb_data.new(url_name=url_name))
    )


def get_ikb_skills_pagination(url_name: str, skill_num: int, max_skills: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()

    row = []

    if skill_num > 1:
        row.append(InlineKeyboardButton(text=f"{skill_num - 1} навык (пред)",
                                        callback_data=hero_skills_pagination_cb_data.new(url_name=url_name,
                                                                                         skill_num=skill_num - 1)))

    if skill_num < max_skills:
        row.append(InlineKeyboardButton(text=f"{skill_num + 1} навык (след)",
                                        callback_data=hero_skills_pagination_cb_data.new(url_name=url_name,
                                                                                         skill_num=skill_num + 1)))
    ikb.add(*row)
    ikb.add(InlineKeyboardButton(text="◀️ Назад",
                                 callback_data=hero_skills_pagination_cb_data.new(url_name=url_name,
                                                                                  skill_num=0)))

    return ikb


def get_ikb_back_to_hero(url_name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="◀️ Назад", callback_data=hero_skills_pagination_cb_data.new(url_name=url_name,
                                                                                               skill_num=0))
    )
