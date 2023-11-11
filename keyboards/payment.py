from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config

ikb_payment_offer = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text=f"Оформить подписку ({config.SUBSCRIBTION_COST_MESSAGE})", callback_data='payment_offer')
)


def ikb_payment(link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="Оплатить", url=link)
    ).add(
        InlineKeyboardButton(text="Проверить оплату", callback_data='check_payment')
    )
