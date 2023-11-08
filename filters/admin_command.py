from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from config import BOT_ADMINS


class AdminCommand(BoundFilter):
    async def check(self, message: types.Message):
        user_id = message.from_user.id
        return str(user_id) in BOT_ADMINS
