from aiogram import types

from filters import UserCommand
from keyboards.payment import get_ikb_payment
from loader import dp
import services.db_commands.subscription as db_sub
import services.db_commands.users as db_users
from utils import text
from utils.misc.throttling import rate_limit

SUBSCRIBTION_COST = 249


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

    answer = text(
        f"👤 Имя: {message.from_user.full_name}",
        f"🏷 UID: {user_id}",
        "",
        f"📅 Начался пользоваться ботом: {created_at}",
        f"Отправлено команд боту: {await db_users.get_user_command_count(user_id)}",
        "",
        f"Осталось бесплатных пиков сегодня: {await db_users.get_user_max_picks_per_day(user_id)}",
        f"💵 Подписка: {sub_expires_date}"
    )

    if not await db_sub.is_user_sub(user_id):
        await message.answer(answer, reply_markup=get_ikb_payment(SUBSCRIBTION_COST))
    else:
        await message.answer(answer)


@dp.callback_query_handler(text='payment')
async def callback_payment(call: types.CallbackQuery):
    await call.message.answer('Оформление платежа')
