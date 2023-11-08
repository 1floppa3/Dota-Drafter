import shutil
from asyncio import sleep
from pathlib import Path

from data.dota2_heroes import DOTA2_HEROES
from utils.dotabuff import parse_hero_data, parse_meta_data
from utils.notify_admins import log_to_admins


async def daily_dotabuff_parser(dp):
    await log_to_admins(dp, "Ежедневный парсинг всех героев и меты... Смотрите подробности в консоли.")
    path = Path("data/dota2_heroes_stats")
    shutil.rmtree(path, True)
    path.mkdir(exist_ok=True)
    for hero in DOTA2_HEROES.keys():
        parse_hero_data(hero)
    await log_to_admins(dp, "Парсинг героев завершён.")

    await sleep(3.0)

    await log_to_admins(dp, "Парсинг меты...")
    path = Path("data/heroes_meta.json")
    path.unlink(True)
    parse_meta_data()
    await log_to_admins(dp, "Парсинг меты завершён.")