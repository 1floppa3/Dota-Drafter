from aiogram import types
from aiogram.types import ParseMode, InputFile
from loguru import logger

from data.dota2_heroes import DOTA2_HEROES
from data.messages import START_MESSAGE
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
        if args in DOTA2_HEROES.keys():
            await hook_argument_hero_data(message, args)
    else:
        logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) /start")
        kb = await kb_main_menu(message.from_user.id)
        await message.answer(START_MESSAGE, parse_mode=ParseMode.HTML, reply_markup=kb)
