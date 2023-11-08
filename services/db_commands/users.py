from datetime import datetime

from aiogram import types, Dispatcher
from loguru import logger

from models.models import Users
from services.db_commands import base_commands as db_base
from utils.exceptions import UserNotFound
from utils.notify_admins import notify_new_user


async def update_user(dp: Dispatcher, message: types.Message):
    try:
        user = await db_base.select_user(message.from_user.id)
        if user is None:
            raise UserNotFound

        command_count = user.command_count
        if command_count is None:
            command_count = 0

        await user.update(is_active=True,
                          username=message.from_user.username,
                          name=message.from_user.full_name,
                          command_count=command_count + 1).apply()
    except UserNotFound:
        await add_new_user(dp, message)
    except Exception as e:
        logger.exception(e)


async def add_new_user(dp: Dispatcher, message: types.Message):
    try:
        await db_base.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
        await notify_new_user(dp, message)
    except Exception as e:
        logger.error(f"Ошибка добавления нового пользователя в БД ({e})")


async def update_user_active(user: Users, active: bool, message: types.Message = None):
    if message is not None:
        await user.update(is_active=active,
                          username=message.from_user.username,
                          name=message.from_user.full_name).apply()
    else:
        await user.update(is_active=active).apply()


async def get_user_command_count(user_id: int) -> int:
    user = await db_base.select_user(user_id)
    return user.command_count


async def get_user_created_date(user_id: int) -> datetime:
    user = await db_base.select_user(user_id)
    return user.created_at


async def get_user_max_picks_per_day(user_id: int) -> int:
    user = await db_base.select_user(user_id)
    return user.max_picks_per_day


async def update_user_max_picks_per_day(*, user: Users = None, user_id: int = 0, num: int = 0):
    try:
        if user is None:
            user = await db_base.select_user(user_id)
        await user.update(max_picks_per_day=num).apply()
    except Exception:
        pass
