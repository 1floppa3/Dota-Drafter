from datetime import datetime

from services.db_commands import base_commands as db_base


async def is_user_sub(user_id: int) -> bool:
    user = await db_base.select_user(user_id)
    return user.is_sub


async def sub_expires_date(user_id: int) -> datetime:
    user = await db_base.select_user(user_id)
    return user.sub_expires
