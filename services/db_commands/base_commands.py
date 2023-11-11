from services.database import db
from services.db_models.models import Users


async def add_user(user_id: int, username: str = None, name: str = None):
    user = Users(user_id=user_id, is_active=True, is_sub=False, username=username, name=name,
                 command_count=0, max_picks_per_day=5)
    await user.create()


async def select_all_users():
    users = await Users.query.gino.all()
    return users


async def users_count() -> int:
    count = await db.func.count(Users.user_id).gino.scalar()
    return count


async def subscribers_count() -> int:
    count = await db.select([db.func.count()]).where(Users.is_sub).gino.scalar()
    return count


async def active_count() -> int:
    count = await db.select([db.func.count()]).where(Users.is_active).gino.scalar()
    return count


async def select_user(user_id: int) -> Users:
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    return user
