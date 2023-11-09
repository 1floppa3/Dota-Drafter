from aiogram import types
from aiogram.types import ParseMode
from loguru import logger

from data import config, dota2
from filters import UserCommand
from handlers.commands.hero_data import hook_argument_hero_data
from keyboards.menu import kb_main_menu
from loader import dp
from utils.misc.throttling import rate_limit


@rate_limit(1, 'start')
@dp.message_handler(UserCommand(), commands=['start'])
async def command_start(message: types.Message):
    args = message.get_args()
    if args != "":
        if args in dota2.heroes.keys():
            await hook_argument_hero_data(message, args)
    else:
        logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) /start")
        kb = await kb_main_menu(message.from_user.id)

        text = (
            f"<b>{config.BOT_NAME.upper()} BOT</b>\n"
            "\n"
            "Бот-помощник для поднятия рейтинга в Dota 2\n"
            "\n"
            "<b><i>🔍 Помощь: /help</i></b>\n"
            "\n"
            f"<b>Канал бота: {config.CHANNEL_LINK}</b>"
        )

        await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=kb)
