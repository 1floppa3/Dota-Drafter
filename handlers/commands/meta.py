from aiogram import types
from aiogram.types import ParseMode, InputFile
from loguru import logger

from data import config, dota2
from filters import UserCommand
from loader import dp
from utils.dotabuff import match_hero_name, parse_meta_data
from utils.misc.throttling import rate_limit


@rate_limit(1, 'meta')
@dp.message_handler(UserCommand(), text=f"🔝 Мета ({dota2.patch})")
@dp.message_handler(UserCommand(), commands=['meta'])
async def command_meta(message: types.Message):
    meta = parse_meta_data()

    winrate_top = sorted(meta.items(), key=lambda x: x[1][0], reverse=True)

    pick_freq_top = sorted(meta.items(), key=lambda x: x[1][1], reverse=True)

    answer = "<b>Текущая мета персонажей:</b>\n"

    answer += "\n<i>По винрейту (Winrate)</i>\n"
    for name, value in winrate_top[:config.WINRATE_TOP_NUM]:
        answer += (f"<a href='https://t.me/{config.BOT_LINK[1:]}?start={match_hero_name(name)}'>{name}</a>: "
                   f"{round(value[0], 2)}%\n")
    answer += '...\n'
    for name, value in reversed(list(reversed(winrate_top))[:config.WINRATE_TOP_NUM // 2]):
        answer += (f"<a href='https://t.me/{config.BOT_LINK[1:]}?start={match_hero_name(name)}'>{name}</a>: "
                   f"{round(value[0], 2)}%\n")

    answer += "\n<i>По частоте выбора (Frequency)</i>\n"
    for name, value in pick_freq_top[:config.FREQUENCY_TOP_NUM]:
        answer += (f"<a href='https://t.me/{config.BOT_LINK[1:]}?start={match_hero_name(name)}'>{name}</a>: "
                   f"{round(value[1], 2)}%\n")
    answer += '...\n'
    for name, value in reversed(list(reversed(pick_freq_top))[:config.FREQUENCY_TOP_NUM // 2]):
        answer += (f"<a href='https://t.me/{config.BOT_LINK[1:]}?start={match_hero_name(name)}'>{name}</a>: "
                   f"{round(value[1], 2)}%\n")

    hero_name = None
    for url_name, data in dota2.heroes.items():
        if data[1] == winrate_top[0][0]:
            hero_name = url_name

    if hero_name is not None:
        photo = InputFile(path_or_bytesio=f"media/dota2_heroes/{hero_name}.png")
        await message.answer_photo(photo, answer, parse_mode=ParseMode.HTML)
    else:
        await message.answer(answer, parse_mode=ParseMode.HTML)

    logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) Успешно /meta!")
