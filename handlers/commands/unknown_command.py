import difflib

from aiogram import types
from loguru import logger

from data import config
from loader import dp
from services.db_commands import users as db_users
from utils.misc.throttling import rate_limit


@rate_limit(1, 'unknown')
@dp.message_handler()
async def unknown_command(message: types.Message):
    await db_users.update_user(dp, message)

    if message.text[0] == '/':
        most_similar = find_most_similar_command(message.text[1:])
        logger.info(
            f"{message.from_user.full_name} (@{message.from_user.username}) Неизвестная команда: {message.text} "
            f"({most_similar})")
        await message.answer(f"Неизвестная команда. Возможно вы имели в виду команду /{most_similar}?")
    else:
        logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) Неизвестный текст: {message.text}")
        await message.answer("Бот не может вас понять.\nПомощь по боту: /help")


def find_most_similar_command(input_str):
    similarity_scores = [(difflib.SequenceMatcher(None, input_str, s).ratio(), s) for s in config.BOT_COMMANDS.keys()]
    similarity_scores.sort(reverse=True)
    return similarity_scores[0][1]
