from aiogram import types, Dispatcher

from config import BOT_COMMANDS


async def set_default_commands(dp: Dispatcher):
    commands_list = []
    for cmd, description in BOT_COMMANDS.items():
        commands_list.append(types.BotCommand(cmd, description))

    await dp.bot.set_my_commands(commands_list)
