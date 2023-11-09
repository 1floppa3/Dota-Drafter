from aiogram import types

from loader import dp


@dp.callback_query_handler(text='payment')
async def callback_payment(call: types.CallbackQuery):
    await call.answer('Оформление платежа')
    await call.message.answer('Оформление платежа')
