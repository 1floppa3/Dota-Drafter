from sqlalchemy.sql.expression import and_

from services.db_models.models import Payments


async def create_payment(user_id: int) -> Payments:
    payment = Payments(user_id=user_id)
    return await payment.create()


async def find_user_payment(user_id: int, is_active: bool, paid: bool) -> Payments:
    return await Payments.query.where(and_(Payments.user_id == user_id,
                                           Payments.is_active == is_active,
                                           Payments.paid == paid)).order_by(Payments.id.desc()).gino.first()


async def select_payment(idx: int) -> Payments:
    return await Payments.query.where(Payments.id == idx).gino.first()


async def change_payment_status(idx: int, is_active: bool | None = None, paid: bool | None = None):
    payment = await select_payment(idx)
    if is_active is not None:
        await payment.update(is_active=is_active).apply()
    if paid is not None:
        await payment.update(paid=paid).apply()
