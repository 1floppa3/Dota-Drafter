from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import CancelHandler

from data import config
from services.db_commands import subscription as db_sub


class SubscriberCommand(BoundFilter):
    async def check(self, message: types.Message):
        user_id = message.from_user.id

        if str(user_id) in config.BOT_ADMINS:
            return True

        if not await db_sub.is_user_sub(user_id):
            await message.answer("🙁 Данная команда доступна только для людей, оформивших платную подписку на бот.\n"
                                 "Подробнее о подписке: /sub")
            raise CancelHandler
        return True
