from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_ikb_payment(price: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text=f"Оформить подписку ({price})", callback_data='payment')
    )
