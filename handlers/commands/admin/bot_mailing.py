from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, RetryAfter, UserDeactivated
from loguru import logger

from filters import AdminCommand
from keyboards.mailing import ikb_mailing_add_next_quit, ikb_mailing_next_quit, ikb_mailing_quit
from loader import dp
from states import BotMailingState
from utils.notify_admins import log_to_admins
from services.db_commands import base_commands as db_base
from services.db_commands import users as db_users


@dp.message_handler(AdminCommand(), commands=['mailing'])
async def command_mailing(message: types.Message):
    await message.answer(f"Введите текст рассылки:")
    await BotMailingState.text.set()


@dp.message_handler(state=BotMailingState.text)
async def mailing_text(message: types.Message, state: FSMContext):
    asnwer = message.text
    await state.update_data(text=asnwer)
    await message.answer(text=asnwer, reply_markup=ikb_mailing_add_next_quit)
    await BotMailingState.state.set()


@dp.callback_query_handler(text='next_step_mailing', state=BotMailingState.state)
async def start_mailing(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    await state.finish()

    await proccess_mailing(call, text)


@dp.callback_query_handler(text='add_photo', state=BotMailingState.state)
async def callback_add_photo(call: types.CallbackQuery):
    await call.message.answer('Пришлите фото')
    await BotMailingState.photo.set()


@dp.message_handler(state=BotMailingState.photo, content_types=types.ContentType.PHOTO)
async def add_photo(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await message.answer_photo(photo=photo, caption=text, reply_markup=ikb_mailing_next_quit)


@dp.callback_query_handler(text='next_step_mailing', state=BotMailingState.photo)
async def start_mailing(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await state.finish()

    await proccess_mailing(call, text, photo)


@dp.message_handler(state=BotMailingState.photo)
async def no_photo(message: types.Message):
    await message.answer("Пришли фотографию", reply_markup=ikb_mailing_quit)


@dp.callback_query_handler(text='quit_mailing',
                           state=[BotMailingState.text, BotMailingState.photo, BotMailingState.state])
async def quit_mailing(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Рассылка отменена")


async def proccess_mailing(call: types.CallbackQuery, text: str, photo=None):
    users = await db_base.select_all_users()

    count = {'success': 0, 'blocked': 0, 'user_not_found': 0, 'user_deactivated': 0}

    for user in users:
        try:
            user = await db_base.select_user(user.user_id)
            if photo is None:
                await dp.bot.send_message(chat_id=user.user_id, text=text)
            else:
                await dp.bot.send_photo(chat_id=user.user_id, photo=photo, caption=text)
        except BotBlocked:
            count['blocked'] += 1
            user.update(is_active=False)
            await db_users.update_user_active(user, False)
            await sleep(0.1)
        except ChatNotFound:
            count['user_not_found'] += 1
            await db_users.update_user_active(user, False)
            await sleep(0.1)
        except RetryAfter as e:
            await sleep(e.timeout * 0.1)
        except UserDeactivated:
            count['user_deactivated'] += 1
            await db_users.update_user_active(user, False)
            await sleep(0.1)
        except Exception as e:
            logger.exception(e)
        else:
            count['success'] += 1
            await db_users.update_user_active(user, True)
            await sleep(0.1)

    if photo is None:
        await call.message.answer(f"Рассылка выполнена \n(инфо: {count})")
        await log_to_admins(dp, f"Рассылка выполнена \n(инфо: {count})\n#mailing")
    else:
        await call.message.answer(f"Рассылка с фото выполнена \n(инфо: {count})")
        await log_to_admins(dp, f"Рассылка с фото выполнена \n(инфо: {count})\n#mailing")
