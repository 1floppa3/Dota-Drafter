import json
from pathlib import Path
from pprint import pprint

import bs4
import pandas as pd
import requests
from fake_useragent import UserAgent
from loguru import logger

from data.dota2_heroes import DOTA2_HEROES
from utils.exceptions import NotEnoughHeroesToAnalyze, WrongHero


def match_hero_name(user_hero: str) -> str:
    user_hero = ''.join(filter(str.isalnum, user_hero.lower()))

    for url_name, data in DOTA2_HEROES.items():
        if user_hero in data[2:] or user_hero == url_name:
            return url_name
    return user_hero


def check_valid_heroes(heroes: list[str]):
    for hero in heroes:
        if hero not in list(DOTA2_HEROES.keys()):
            raise WrongHero(hero)


def parse_hero_data(name: str) -> dict:
    url = f"https://ru.dotabuff.com/heroes/{name}/counters?date=week"
    user_agent = str(UserAgent().random)

    result = open_hero_data(name)
    if result is not None:
        return result

    result = {}

    try:
        page = requests.get(url, headers={"User-Agent": user_agent})
        dataframe = pd.read_html(page.text)
        stats_table = list(dataframe[3].values)
        for i in range(len(stats_table)):
            hero_name = stats_table[i][1]
            lose_rate = float(stats_table[i][2].replace('%', ''))
            win_rate = float(stats_table[i][3].replace('%', ''))
            result[hero_name] = [lose_rate, win_rate]
    except Exception:
        raise WrongHero(name)

    url = f"https://ru.dotabuff.com/heroes/{name}?date=week"
    try:
        page = requests.get(url, headers={"User-Agent": user_agent})
        dataframe = pd.read_html(page.text)

        hero_attributes_table = dataframe[8].values
        result['strength_attr'] = hero_attributes_table[1][0]
        result['agility_attr'] = hero_attributes_table[1][1]
        result['intelligence_attr'] = hero_attributes_table[1][2]

        hero_stats_table = dataframe[9].values
        result['movement_speed'] = hero_stats_table[0][1]
        result['sight_range'] = hero_stats_table[1][1]
        result['armor'] = hero_stats_table[2][1]
        result['base_attack_time'] = hero_stats_table[3][1]
        result['damage'] = hero_stats_table[4][1]
        result['attack_point'] = hero_stats_table[5][1]
    except Exception:
        raise WrongHero(name)

    try:
        url = f"https://ru.dotabuff.com/heroes/{name}/abilities"
        page = requests.get(url, headers={"User-Agent": user_agent})

        dataframe = pd.read_html(page.text)

        talents = {}
        talents_table = dataframe[0].values
        for talent in talents_table:
            talents[f'talent_{talent[1]}'] = {
                'left': talent[0],
                'right': talent[2]
            }

        soup = bs4.BeautifulSoup(page.text, "html.parser")

        skills = {}
        header, article = [], []
        i = 0
        for skill_section in list(soup.select('section'))[:-3]:
            for skill_header in skill_section.select('header'):
                skill_key = ''
                for key in skill_header.select('big'):
                    skill_key = key.text
                if skill_key:
                    skill_name = skill_header.text[:-1]
                else:
                    skill_key = "Passive"
                    skill_name = skill_header.text

                header.append([skill_name, skill_key])

            for skill_article in skill_section.select('article'):
                effects = []
                for skill_effects in skill_article.select('.effects'):
                    for skill_effect in skill_effects.select('p'):
                        effects.append(skill_effect.text)

                description = ''
                for skill_description in skill_article.select('.description > p'):
                    description = skill_description.text

                stats = []
                for skill_stats in skill_article.select('.stats'):
                    for skill_stat in skill_stats.select('.stat'):
                        stats.append(skill_stat.text)

                cooldown, manacost = '', ''
                for skill_cooldown in skill_article.select('.cooldown'):
                    cooldown = skill_cooldown.text
                for skill_manacost in skill_article.select('.manacost'):
                    manacost = skill_manacost.text

                lore = ''
                for skill_lore in skill_article.select('.lore'):
                    lore = skill_lore.text

                article.append([effects, description, stats, cooldown, manacost, lore])

            skills[f'skill_{i + 1}'] = {
                'name': header[i][0],
                'key': header[i][1],
                'effects': article[i][0],
                'description': article[i][1],
                'stats': article[i][2],
                'cooldown': article[i][3],
                'manacost': article[i][4],
                'lore': article[i][5],
            }
            i += 1
    except Exception:
        raise WrongHero(name)

    result.update(skills)
    result.update(talents)
    save_hero_data(name, result)
    return result


def open_hero_data(name: str) -> dict | None:
    try:
        with open(Path(f"data/dota2_heroes_stats/{name}.json"), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def save_hero_data(name: str, res: dict):
    with open(Path(f"data/dota2_heroes_stats/{name}.json"), 'w') as file:
        json.dump(res, file, indent=4)
    logger.info(f"Сохранение данных персонажа {name}.")


def parse_meta_data():
    url = "https://ru.dotabuff.com/heroes/meta?date=week"
    user_agent = str(UserAgent().random)

    res = open_meta_data()
    if res is not None:
        return res

    result = {}

    try:
        page = requests.get(url, headers={"User-Agent": user_agent})
        dataframe = pd.read_html(page.text)
        stats_table = list(dataframe[0].values)

        for i in range(len(stats_table)):
            hero_name = stats_table[i][1]
            pick_freq = float(stats_table[i][10].replace('%', ''))
            win_rate = float(stats_table[i][11].replace('%', ''))
            result[hero_name] = [win_rate, pick_freq]
    except (ValueError, Exception):
        print("Failed to save meta data!!!")
        return

    save_meta_data(result)

    return result


def open_meta_data() -> dict | None:
    try:
        with open(Path(f"data/heroes_meta.json"), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def save_meta_data(res: dict):
    with open(Path(f"data/heroes_meta.json"), 'w') as file:
        json.dump(res, file, indent=4)
    logger.info(f"Сохранение меты героев.")


def find_counter_picks(heroes: list[str]) -> dict[str, float]:
    heroes = list(set(heroes))

    if len(heroes) < 1:
        raise NotEnoughHeroesToAnalyze

    result = {}
    for hero, data in parse_hero_data(heroes[0]).items():
        if hero not in [full_name[1] for full_name in DOTA2_HEROES.values()]:
            continue
        result[hero] = data[0]

    for i in range(1, len(heroes)):
        cur_hero = {}
        for hero, data in parse_hero_data(heroes[i]).items():
            if hero not in [full_name[1] for full_name in DOTA2_HEROES.values()]:
                continue
            cur_hero[hero] = data[0]

        result = {k: result.get(k, 0) + cur_hero.get(k, 0) for k in result}

    for url_name, data in DOTA2_HEROES.items():
        if url_name in heroes and data[1] in result:
            del result[data[1]]

    return result


def rm_hero_winrate(res: dict[str, list[float, float]]) -> dict[str, float]:
    out = {}
    for hero, data in res.items():
        data.pop()
        out[hero] = data[0]
    return out


def determine_match_winner(first_team: list[str], second_team: list[str]):
    temp = []
    for url_name, data in DOTA2_HEROES.items():
        if url_name in second_team:
            temp.append(data[1].strip())

    second_team = temp

    hero_rates = []
    for team1_hero in first_team:
        team1_hero_data = parse_hero_data(team1_hero)
        rate_sum = 0
        for team2_hero_name in second_team:
            rate_sum += team1_hero_data[team2_hero_name][1] - 50
        hero_rates.append(rate_sum)
    sum_rate = sum(hero_rates)
    return sum_rate


if __name__ == "__main__":
    parse_hero_data('sven')
