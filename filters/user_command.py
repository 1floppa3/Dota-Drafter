from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import CancelHandler

from data import config
from keyboards.channel_subscriber import get_ikb_channels_to_subscribe
from loader import bot, dp
from services.db_commands import users as db_users


class UserCommand(BoundFilter):
    async def check(self, message: types.Message):
        await db_users.update_user(dp, message)

        if config.API_TOKEN == "6399663929:AAEIeIKSgGo4a4Id3X2hooiigjqmCEDwEPM":
            return True
        # TODO in final version delete lines above

        for data in config.SUBSCRIBER_CHECK.values():
            sub = await bot.get_chat_member(chat_id=data[0], user_id=message.from_user.id)
            if sub.status == types.ChatMemberStatus.LEFT:
                ikb = await get_ikb_channels_to_subscribe(message.from_user.id)
                await message.answer("Подпишитесь на канал(ы) и повторите попытку:\n", reply_markup=ikb)
                raise CancelHandler

        return True
