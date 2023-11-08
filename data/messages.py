from aiogram.utils.markdown import hlink

import config
from config import BOT_NAME
from utils import text

START_MESSAGE = text(
    f"<b>{BOT_NAME.upper()} BOT</b>",
    "",
    "Бот-помощник для поднятия рейтинга в Dota 2",
    "",
    "<b><i>🔍 Помощь: /help</i></b>",
    "",
    f"<b>Канал бота: {config.CHANNEL_LINK}</b>"
)

HELP_MESSAGE = text(
    f"<b>Бот-помощник для поднятия рейтинга в Dota 2</b>",
    "",
    "<b><u>Список команд:</u></b>",
    "<b>/start</b> - <i>перезапуск бота</i>",
    "<b>/help</b> - <i>помощь по боту</i>",
    "<b>/profile</b> - <i>профиль</i>",
    "<b>/pick (алиас: /p)</b> - <i>подобрать контр-пик команде или герою</i>",
    "<b>/meta</b> - <i>список лучших героев по винрейту, популярности и статистике</i>",
    "🆕 <b>/heroes</b> - <i>список всех героев</i>",
    "🆕 <b>/sub</b> - <i>информация о платной подписке</i>",
    "",
    "<u>Платный функционал:</u>",
    "<b>/pick_teams (алиас: /pt)</b> - <i>анализ пиков двух команд, выявление перевеса по пику</i>",
    "",
    "<b><u>Информация:</u></b>",
    f"<i>Версия бота: {config.BOT_VERSION}</i>",
    f"<i>Dota2 Patch: {config.DOTA2_PATCH}</i>",
    "",
    f"<b>Канал бота: {config.CHANNEL_LINK}</b>",
    "<i>Связь: @floppa13 (кодер)</i>",
    "<i>По поводу сотрудничества, улучшения бота, багам писать кодеру!</i>"
)

UNKNOWN_TEXT_MESSAGE = text(
    "Бот не может вас понять.",
    "Помощь по боту: /help"
)


def UNKNOWN_COMMAND_MESSAGE(most_similar_command: str) -> str:
    return text(
        f"Неизвестная команда. Возможно вы имели в виду команду /{most_similar_command}?"
    )
