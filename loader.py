import sys

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import ValidationError
from loguru import logger

import config
from services.database import db

try:
    bot = Bot(token=config.API_TOKEN)
except ValidationError:
    logger.error('Cannot find API_TOKEN')
    sys.exit()

dp = Dispatcher(bot, storage=MemoryStorage())

__all__ = ['bot', 'dp', 'db']
