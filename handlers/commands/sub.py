from aiogram import types
from aiogram.types import ParseMode
from loguru import logger

import services.db_commands.subscription as db_sub
import services.db_commands.users as db_users
from data import config
from filters import UserCommand
from keyboards.payment import ikb_payment_offer
from loader import dp
from utils.misc.throttling import rate_limit


@rate_limit(1, 'sub')
@dp.message_handler(UserCommand(), text="💵 Подписка")
@dp.message_handler(UserCommand(), commands=['sub', 'subscription'])
async def command_meta(message: types.Message):
    user_id = message.from_user.id

    if await db_sub.is_user_sub(user_id):
        date = await db_sub.sub_expires_date(user_id)
        sub_expires_date = 'активна до ' + date.strftime("%d/%m/%Y")
    else:
        sub_expires_date = 'не активна'

    created_at_date = await db_users.get_user_created_date(user_id)
    created_at = created_at_date.strftime("%d/%m/%Y")

    text = (f"<i>💵 Подписка: <b>{sub_expires_date}</b></i>\n"
            "\n"
            "<u>Информация о платной подписке:</u>\n"
            "<b>Функции:</b>\n"
            "<i>• Неограниченное количество использований команды /pick</i>\n"
            "<i>• Команда /pick_teams (анализ пиков сразу двух команд)</i>\n"
            "<i>• Просмотр против кого герой хорош или плох (/heroes)</i>\n"
            "\n"
            "🙏 Покупая подписку вы сильно помогаете разработчикам, поддерживаете бота и разработку будущих продуктов.\n"
            "\n"
            f"<b>Цена: {config.SUBSCRIBTION_COST_MESSAGE}</b>")

    if not await db_sub.is_user_sub(user_id):
        await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=ikb_payment_offer)
    else:
        await message.answer(text, parse_mode=ParseMode.HTML)

    logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) /sub")
