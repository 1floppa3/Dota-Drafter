from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data import config


class AdminCommand(BoundFilter):
    async def check(self, message: types.Message):
        user_id = message.from_user.id
        return str(user_id) in config.BOT_ADMINS
