from aiogram import types
from aiogram.types import ParseMode
from loguru import logger

import services.db_commands.subscription as db_sub
import services.db_commands.users as db_users
from data import config
from filters import UserCommand
from keyboards.payment import get_ikb_payment
from loader import dp
from utils.misc.throttling import rate_limit


@rate_limit(1, 'profile')
@dp.message_handler(UserCommand(), text="👤 Профиль")
@dp.message_handler(UserCommand(), commands=['profile'])
async def command_profile(message: types.Message):
    user_id = message.from_user.id

    if await db_sub.is_user_sub(user_id):
        date = await db_sub.sub_expires_date(user_id)
        sub_expires_date = 'активна до ' + date.strftime("%d/%m/%Y")
    else:
        sub_expires_date = 'не активна'

    created_at_date = await db_users.get_user_created_date(user_id)
    created_at = created_at_date.strftime("%d/%m/%Y")

    text = (f"👤 Имя: {message.from_user.full_name}\n"
            f"📅 Начался пользоваться ботом: {created_at}\n"
            "\n"
            f"<i>Отправлено команд боту: <b>{await db_users.get_user_command_count(user_id)}\n</b></i>"
            f"<i>Осталось бесплатных пиков сегодня: <b>{await db_users.get_user_max_picks_per_day(user_id)}\n</b></i>"
            "\n"
            f"<i>💵 Подписка: <b>{sub_expires_date}</b> (/sub)</i>")

    if not await db_sub.is_user_sub(user_id):
        await message.answer(text, parse_mode=ParseMode.HTML,
                             reply_markup=get_ikb_payment(config.SUBSCRIBTION_COST_MESSAGE))
    else:
        await message.answer(text, parse_mode=ParseMode.HTML)

    logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) /profile")
