from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
from loader import bot


async def get_ikb_channels_to_subscribe(user_id: int):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for channel, data in config.SUBSCRIBER_CHECK.items():
        sub = await bot.get_chat_member(chat_id=data[0], user_id=user_id)
        if sub.status == types.ChatMemberStatus.LEFT:
            keyboard.add(InlineKeyboardButton(channel, url=data[1]))
    return keyboard
