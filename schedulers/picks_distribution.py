from data import config
from services.db_commands import base_commands as db_base
from services.db_commands import users as db_users
from utils.notify_admins import log_to_admins


async def daily_picks_distribution(dp):
    users = await db_base.select_all_users()

    for user in users:
        await db_users.update_user_max_picks_per_day(user=user, num=config.PICKS_PER_DAY)
    await log_to_admins(dp, f"Ежедневная выдача всем пользователям бота {config.PICKS_PER_DAY} пиков выполнена.")
