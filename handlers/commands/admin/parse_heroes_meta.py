import shutil
from asyncio import sleep
from pathlib import Path

from aiogram import types

from data import dota2
from filters import AdminCommand
from loader import dp
from utils.dotabuff import parse_meta_data, parse_hero_data


@dp.message_handler(AdminCommand(), commands=['parse_heroes_meta'])
async def command_parse_heroes_meta(message: types.Message):
    await message.answer(f"Парсинг всех героев и меты. Подробности в консоли.")

    path = Path("data/dota2_heroes_stats")
    shutil.rmtree(path, True)
    path.mkdir(exist_ok=True)
    parse_all_heroes_data()

    await sleep(1.0)

    path = Path("data/heroes_meta.json")
    path.unlink(True)
    parse_meta_data()

    await message.answer(f"Парсинг завершён!")


def parse_all_heroes_data():
    for hero in dota2.heroes.keys():
        parse_hero_data(hero)
