from pprint import pprint

from aiogram import types
from aiogram.types import ParseMode
from aiopayAPI import QuickPay, PayOk

import services.db_commands.payments as db_payments
import services.db_commands.subscription as db_sub
from data import config
from keyboards.payment import ikb_payment
from loader import dp
from utils.notify_admins import log_to_admins


@dp.callback_query_handler(text='payment_offer')
async def callback_payment_offer(call: types.CallbackQuery):
    if (await db_sub.is_user_sub(call.from_user.id) or
            await db_payments.find_user_payment(call.from_user.id, True, True) is not None):
        await call.answer("BUG! Уже есть подписка!")
        return

    payment = await db_payments.find_user_payment(call.from_user.id, True, False)
    if payment is None:
        payment = await db_payments.create_payment(call.from_user.id)

    quick = QuickPay(
        amount=config.SUBSCRIBTION_COST_RUB,
        payment=str(payment.id),
        shop=config.PAYOK_SHOP_ID,
        desc="Подписка на бота Dota Drafter",
        currency="RUB",
        secret=config.PAYOK_SHOP_KEY
    )

    await call.message.edit_text(f"<b>Оформление подписки #{payment.id}\n"
                                 f"Стоимость ({config.SUBSCRIBTION_COST_MESSAGE})</b>\n"
                                 "<i>О подписке: /sub</i>\n"
                                 "\n"
                                 "<i>Используйте кнопки ниже для оплаты платной подписки.</i>",
                                 parse_mode=ParseMode.HTML,
                                 reply_markup=ikb_payment(quick.generate_paylink()))


@dp.callback_query_handler(text='check_payment')
async def callback_check_payment(call: types.CallbackQuery):
    payment = await db_payments.find_user_payment(call.from_user.id, True, False)

    pay = PayOk(
        API_ID=config.PAYOK_API_ID,
        API_KEY=config.PAYOK_API_KEY,
        shop=config.PAYOK_SHOP_ID,
        payment=payment.id
    )

    pprint(await pay.get.balance())
    pprint(await pay.get.payout())

    if "платеж подтвердился":
        await db_payments.change_payment_status(payment.id, is_active=False, paid=True)
        date = await db_sub.give_sub(call.from_user.id)
        await call.message.answer("<b>Благодарим вас за покупку платной подписки!</b>\n"
                                  f"<i>Дата окончания: {date.strftime('%d/%m/%Y')}</i>", parse_mode=ParseMode.HTML)

        await log_to_admins(dp, "📄 Пользователь "
                                f"(<a href='tg://user?id={call.from_user.id}'>{call.from_user.full_name}</a> "
                                f"(@{call.from_user.username}) #{call.from_user.id}) "
                                f"приобрёл подписку за {config.SUBSCRIBTION_COST_RUB} руб.", log=False)
    else:
        await call.answer("Платёж не найден.")
