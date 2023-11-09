from aiogram import executor, Dispatcher
from loguru import logger

import filters
import middlewares
import schedulers
from handlers import dp
from services import database
from services.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify, on_shutdown_notify


async def on_startup(dispatcher: Dispatcher):
    filters.setup(dispatcher)
    middlewares.setup(dispatcher)

    await database.setup_connection()
    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)


async def on_shutdown(dispatcher: Dispatcher):
    await database.close_connection()
    await on_shutdown_notify(dispatcher)


if __name__ == '__main__':
    logger.add('logs.log', rotation='00:00', compression='zip', retention=7)
    schedulers.setup(dp)
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
