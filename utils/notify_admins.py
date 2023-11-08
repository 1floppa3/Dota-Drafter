from loguru import logger

from aiogram import Dispatcher, types

import config


async def log_to_admins(dp: Dispatcher, message: str):
    logger.info(message)

    try:
        await dp.bot.send_message(config.GROUP_TO_LOG, message)
    except Exception as e:
        logger.error(e)


async def notify_new_user(dp: Dispatcher, message: types.Message):
    logger.info(f"Зарегистрирован новый пользователь #{message.from_user.id}\n"
                f"{message.from_user.full_name} (@{message.from_user.username})")

    try:
        await dp.bot.send_message(config.GROUP_TO_LOG,
                                  f"Зарегистрирован новый пользователь #{message.from_user.id}\n"
                                  f"{message.from_user.full_name} (@{message.from_user.username})")
    except Exception as e:
        logger.error(e)


async def on_startup_notify(dp: Dispatcher):
    logger.info("Бот запущен.")

    try:
        await dp.bot.send_message(config.GROUP_TO_LOG, "Бот запущен.")
    except Exception as e:
        logger.error(e)


async def on_shutdown_notify(dp: Dispatcher):
    logger.info("Бот выключен.")

    try:
        await dp.bot.send_message(config.GROUP_TO_LOG, "Бот выключен.")
    except Exception as e:
        logger.error(e)
