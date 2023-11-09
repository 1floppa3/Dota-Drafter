from aiogram import types
from aiogram.types import ParseMode
from loguru import logger

from data import config, dota2
from filters import UserCommand
from loader import dp
from utils.misc.throttling import rate_limit


@rate_limit(1, 'help')
@dp.message_handler(UserCommand(), text="🔍 Помощь")
@dp.message_handler(UserCommand(), commands=['help'])
async def command_help(message: types.Message):
    logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) /help")

    text = (
        f"<b>Бот-помощник для поднятия рейтинга в Dota 2</b>\n"
        "\n"
        "<b><u>Список команд:</u></b>\n"
        "<b>/start</b> - <i>перезапуск бота</i>\n"
        "<b>/help</b> - <i>помощь по боту</i>\n"
        "<b>/profile</b> - <i>профиль</i>\n"
        "<b>/pick (алиас: /p)</b> - <i>подобрать контр-пик команде или герою</i>\n"
        "<b>/meta</b> - <i>список лучших героев по винрейту, популярности и статистике</i>\n"
        "🆕 <b>/heroes</b> - <i>список всех героев</i>\n"
        "🆕 <b>/sub</b> - <i>информация о платной подписке</i>\n"
        "\n"
        "<u>Платный функционал:</u>\n"
        "<b>/pick_teams (алиас: /pt)</b> - <i>анализ пиков двух команд, выявление перевеса по пику</i>\n"
        "\n"
        "<b><u>Информация:</u></b>\n"
        f"<i>Версия бота: {config.BOT_VERSION}</i>\n"
        f"<i>Dota2 Patch: {dota2.patch}</i>\n"
        "\n"
        f"<b>Канал бота: {config.CHANNEL_LINK}</b>\n"
        "<i>Связь: @floppa13 (кодер)</i>\n"
        "<i>По поводу сотрудничества, улучшения бота, багам писать кодеру!</i>\n"
    )

    await message.answer(text, parse_mode=ParseMode.HTML)
