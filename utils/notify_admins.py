from aiogram import Dispatcher, types
from aiogram.types import ParseMode
from loguru import logger

from data import config


async def log_to_admins(dp: Dispatcher, text: str, log=True):
    if log:
        logger.info(text)

    try:
        await dp.bot.send_message(config.GROUP_TO_LOG, text)
    except Exception as e:
        logger.error(e)


async def notify_new_user(dp: Dispatcher, message: types.Message):
    logger.info("Зарегистрирован новый пользователь "
                f"({message.from_user.full_name}</a> "
                f"(@{message.from_user.username}) #{message.from_user.id}\n)")

    try:
        await dp.bot.send_message(config.GROUP_TO_LOG,
                                  "Зарегистрирован новый пользователь "
                                  f"(<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a> "
                                  f"(@{message.from_user.username}) #{message.from_user.id}\n)",
                                  parse_mode=ParseMode.HTML)
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
