from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_ikb_payment(price: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text=f"Оформить подписку ({price} руб/месяц)", callback_data='payment')
    )
