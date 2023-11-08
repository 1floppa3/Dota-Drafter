from aiogram import types
from loguru import logger
import difflib

from config import BOT_COMMANDS
from data.messages import UNKNOWN_COMMAND_MESSAGE, UNKNOWN_TEXT_MESSAGE
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
        await message.answer(UNKNOWN_COMMAND_MESSAGE(most_similar))
    else:
        logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) Неизвестный текст: {message.text}")
        await message.answer(UNKNOWN_TEXT_MESSAGE)


def find_most_similar_command(input_str):
    similarity_scores = [(difflib.SequenceMatcher(None, input_str, s).ratio(), s) for s in BOT_COMMANDS.keys()]
    similarity_scores.sort(reverse=True)
    return similarity_scores[0][1]
