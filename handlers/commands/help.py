from aiogram import types
from aiogram.types import ParseMode
from loguru import logger

from data.messages import HELP_MESSAGE
from filters import UserCommand
from loader import dp
from utils.misc.throttling import rate_limit


@rate_limit(1, 'help')
@dp.message_handler(UserCommand(), text="🔍 Помощь")
@dp.message_handler(UserCommand(), commands=['help'])
async def command_help(message: types.Message):
    logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) /help")
    await message.answer(HELP_MESSAGE, parse_mode=ParseMode.HTML)
