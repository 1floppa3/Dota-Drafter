from aiogram import executor, Dispatcher
from loguru import logger

import filters
import middlewares
import schedulers
import config
from handlers import dp
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from services.set_bot_commands import set_default_commands

from loader import db


async def on_startup(dispatcher: Dispatcher):
    filters.setup(dispatcher)
    middlewares.setup(dispatcher)

    try:
        logger.info(f"Установка подключения PostgreSQL ({config.POSTGRE_URI})")
        await db.set_bind(config.POSTGRE_URI)
        await db.gino.create_all()
    except Exception as e:
        logger.error(f"Ошибка подключения PostgreSQL ({e})")

    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)


async def on_shutdown(dispatcher: Dispatcher):
    bind = db.pop_bind()
    if bind:
        try:
            logger.info("Закрытие подключения PostgreSQL")
            await bind.close()
        except Exception as e:
            logger.error(f"Ошибка закрытия подключения PostgreSQL ({e})")

    await on_shutdown_notify(dispatcher)


if __name__ == '__main__':
    logger.add('logs.log', rotation='00:00', compression='zip', retention=7)
    schedulers.setup(dp)
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
