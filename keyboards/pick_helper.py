import json
import random
import string
from pathlib import Path

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import config

ikb_allowed_heroes = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text="Список героев", url=config.HERO_NAMES_URL_LINK)
)

replace_hero_cb_data = CallbackData('replace_hero', "filename")
remove_hero_cb_data = CallbackData('remove_hero', "filename")


def get_ikb_wronghero(wrong_hero: str, heroes: list[str]) -> InlineKeyboardMarkup:
    data = {
        "wrong_name": wrong_hero,
        "heroes": heroes
    }

    filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=30)) + '.json'
    path = Path(f"temp/pick/{filename}")
    Path('temp/pick/').mkdir(parents=True, exist_ok=True)

    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        pass

    ikb = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text="Список героев", url=config.HERO_NAMES_URL_LINK)
    ).add(
        InlineKeyboardButton(text=f"Заменить героя {wrong_hero}",
                             callback_data=replace_hero_cb_data.new(filename=filename)),
        InlineKeyboardButton(text=f"Удалить героя {wrong_hero}",
                             callback_data=remove_hero_cb_data.new(filename=filename))
    )

    return ikb
