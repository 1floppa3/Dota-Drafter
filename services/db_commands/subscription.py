from datetime import datetime, timedelta

import pytz

from data import config
from services.db_commands import base_commands as db_base


async def is_user_sub(user_id: int) -> bool:
    user = await db_base.select_user(user_id)
    return user.is_sub


async def sub_expires_date(user_id: int) -> datetime:
    user = await db_base.select_user(user_id)
    return user.sub_expires


async def give_sub(user_id: int) -> datetime:
    user = await db_base.select_user(user_id)
    date = datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=config.SUBSCRIBTION_DAYS)
    date = datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(minutes=2)
    await user.update(is_sub=True, sub_expires=date).apply()
    return date


async def is_sub_expires(user_id: int) -> bool:
    user = await db_base.select_user(user_id)
    return datetime.utcnow().replace(tzinfo=pytz.UTC) > user.sub_expires and user.is_sub


async def remove_sub(user_id: int):
    user = await db_base.select_user(user_id)
    await user.update(is_sub=False).apply()
