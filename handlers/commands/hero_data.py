from aiogram import types
from aiogram.types import ParseMode, InputFile
from loguru import logger

from data.dota2_heroes import DOTA2_HEROES
from filters import UserCommand
from handlers.commands.heroes import heroes_pagination, HEROES_PER_PAGE
from keyboards.hero_data import (get_ikb_hero_data, hero_skills_cb_data, hero_talents_cb_data,
                                 get_ikb_skills_pagination, hero_skills_pagination_cb_data, hero_back_to_heroes_cb_data,
                                 get_ikb_talents)
from keyboards.heroes_pagination import get_ikb_heroes_pagination
from loader import dp
from utils.dotabuff import parse_hero_data, parse_meta_data
from utils.misc.throttling import rate_limit


@rate_limit(1, 'hero_data')
@dp.message_handler(UserCommand(), commands=DOTA2_HEROES.keys())
async def command_hero_data(message: types.Message):
    logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) {message.text}")
    url_name = message.text[1:]
    photo = InputFile(path_or_bytesio=f"media/dota2_heroes/{url_name}.png")
    text = hero_data_message(url_name)
    await message.answer_photo(photo, text, parse_mode=ParseMode.HTML, reply_markup=get_ikb_hero_data(url_name))


async def hook_argument_hero_data(message: types.Message, url_name: str):
    photo = InputFile(path_or_bytesio=f"media/dota2_heroes/{url_name}.png")
    text = hero_data_message(url_name)
    await message.answer_photo(photo, text, parse_mode=ParseMode.HTML, reply_markup=get_ikb_hero_data(url_name))


def hero_data_message(url_name: str) -> str:
    hero_data = parse_hero_data(url_name)
    meta = parse_meta_data()

    text = (f"<b>Герой {DOTA2_HEROES[url_name][1]}</b>\n"
            f"Роли: <i>{', '.join(list(DOTA2_HEROES[url_name][0]))}</i>\n"
            f"<tg-spoiler><i>P.S. Не согласны с ролями? Пожалуйста, "
            f"напишите об этом <a href='https://t.me/floppa13'>кодеру</a></i></tg-spoiler>\n"
            "\n"
            "<i><b><u>Аттрибуты:</u></b>\n"
            f"<b>• Сила: {hero_data['strength_attr']}</b>\n"
            f"<b>• Ловкость: {hero_data['agility_attr']}</b>\n"
            f"<b>• Интеллект: {hero_data['intelligence_attr']}</b>\n"
            "\n"
            f"⊙ Скорость передвижения: <b>{hero_data['movement_speed']}</b>\n"
            f"⊙ Область видимости: <b>{hero_data['sight_range']}</b>\n"
            f"⊙ Броня: <b>{hero_data['armor']}</b>\n"
            f"⊙ Базовое время атаки: <b>{hero_data['base_attack_time']}</b>\n"
            f"⊙ Урон: <b>{hero_data['damage']}</b>\n"
            f"⊙ Время замаха на атаку: <b>{hero_data['attack_point']}</b></i>\n"
            "\n"
            "<i><b><u>Статистика (мета):</u></b>\n"
            f"Винрейт (Winrate): <b>{meta[DOTA2_HEROES[url_name][1]][0]}%</b>\n"
            f"Частота выбора (Frequency): <b>{meta[DOTA2_HEROES[url_name][1]][1]}%</b></i>")

    return text


def hero_skills_pagination(url_name: str, skill_num: int) -> (str, int):
    hero_data = parse_hero_data(url_name)

    text = f"<i><b>{DOTA2_HEROES[url_name][1]}</b>: Навыки (<b>{skill_num}</b>)</i>\n\n"

    hero_skills = []
    for key, value in hero_data.items():
        if "skill" in key:
            hero_skills.append(value)

    skill = hero_skills[skill_num - 1]

    effects = "\n".join(skill['effects'])
    stats = "\n".join(skill['stats'])
    text += (f"<b><u>{skill['name']}</u> ({skill['key']})</b>\n"
             f"<i>{effects}\n\n"
             f"Описание: {skill['description']}\n"
             f"{stats}\n\n")
    if skill['cooldown'] != "":
        text += f"КД: {skill['cooldown']} с"
        if skill['manacost'] != "":
            text += "  |  "
    if skill['manacost'] != "":
        text += f"Манакост: {skill['manacost']}"

    if skill['cooldown'] != "" or skill['manacost'] != "":
        text += "\n\n"

    text += f"{skill['lore']}</i>"
    return text, len(hero_skills)


@dp.callback_query_handler(hero_skills_cb_data.filter())
async def callback_hero_skills(call: types.CallbackQuery, callback_data: dict):
    url_name = callback_data['url_name']
    text, max_skills = hero_skills_pagination(url_name, 1)
    await call.message.edit_caption(text, parse_mode=ParseMode.HTML,
                                    reply_markup=get_ikb_skills_pagination(url_name, 1, max_skills))


@dp.callback_query_handler(hero_skills_pagination_cb_data.filter())
async def callback_hero_skills_pagination(call: types.CallbackQuery, callback_data: dict):
    url_name = callback_data['url_name']
    skill_num = int(callback_data['skill_num'])
    if skill_num == 0:
        text = hero_data_message(url_name)
        await call.message.edit_caption(text, parse_mode=ParseMode.HTML, reply_markup=get_ikb_hero_data(url_name))
    else:
        text, max_skills = hero_skills_pagination(url_name, skill_num)
        await call.message.edit_caption(text, parse_mode=ParseMode.HTML,
                                        reply_markup=get_ikb_skills_pagination(url_name, skill_num, max_skills))


@dp.callback_query_handler(hero_talents_cb_data.filter())
async def callback_hero_talents(call: types.CallbackQuery, callback_data: dict):
    url_name = callback_data['url_name']
    hero_data = parse_hero_data(url_name)

    hero_talents = {}
    for key, value in hero_data.items():
        if "talent" in key:
            hero_talents[key.replace('talent_', '')] = value['left'], value['right']

    text = f"<i><b>{DOTA2_HEROES[url_name][1]}</b>: Таланты</i>\n\n<i>"
    for level, (left, right) in reversed(hero_talents.items()):
        print(level, left, right)
        text += (f"<b>{level} уровень</b>\n"
                 f"Левый     |   {left}\n"
                 f"Правый  |   {right}\n\n")
    text += "</i>"

    await call.message.edit_caption(text, parse_mode=ParseMode.HTML, reply_markup=get_ikb_talents(url_name))


@dp.callback_query_handler(hero_back_to_heroes_cb_data.filter())
async def callback_hero_back_to_heroes(call: types.CallbackQuery, callback_data: dict):
    url_name = callback_data['url_name']
    index = list(DOTA2_HEROES.keys()).index(url_name)

    page = (index // HEROES_PER_PAGE) + 1
    await call.message.delete()
    await call.message.answer(heroes_pagination(page, HEROES_PER_PAGE),
                              parse_mode=ParseMode.HTML,
                              reply_markup=get_ikb_heroes_pagination(page, HEROES_PER_PAGE))

