from aiogram import types

from filters import AdminCommand
from loader import dp
from services.db_commands import base_commands as db_base


@dp.message_handler(AdminCommand(), commands=['users_count'])
async def command_users_count(message: types.Message):
    count = await db_base.users_count()

    active_count = await db_base.active_count()
    subsribers_count = await db_base.subscribers_count()

    await message.answer(f"Количество записей в базе данных: {count}\nАктивных пользователей: {active_count}"
                         f"\nОбладателей подписок: {subsribers_count}")
