from aiogram import types
from aiogram.types import ParseMode
from loguru import logger

from config import BOT_LINK, HEROES_PER_PAGE
from data.dota2_heroes import DOTA2_HEROES
from filters import UserCommand
from keyboards.heroes_pagination import heroes_list_cb_data, get_ikb_heroes_pagination
from loader import dp
from utils.misc.throttling import rate_limit


@rate_limit(1, 'heroes')
@dp.message_handler(UserCommand(), text="📄 Все герои")
@dp.message_handler(UserCommand(), commands=['heroes', 'list'])
async def command_heroes(message: types.Message):
    logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) /heroes")

    await message.answer(heroes_pagination(1, HEROES_PER_PAGE),
                         parse_mode=ParseMode.HTML, reply_markup=get_ikb_heroes_pagination(1, HEROES_PER_PAGE))


def heroes_pagination(page: int, heroes_per_page: int) -> str:
    heroes_list = []
    idx = 0
    for url_name, data in DOTA2_HEROES.items():
        idx += 1
        roles = ', '.join(list(data[0]))
        heroes_list.append(f"<b>{idx}</b> <a href='https://t.me/{BOT_LINK[1:]}?start={url_name}'>{data[1]}</a> "
                           f"<b>({roles})</b>")

    start_index = (page - 1) * heroes_per_page
    end_index = page * heroes_per_page
    heroes_str = '\n'.join(heroes_list[start_index:end_index])

    return f"<i>Список героев <b><u>(стр. {page})</u></b></i>\n{heroes_str}"


@dp.callback_query_handler(heroes_list_cb_data.filter())
async def callback_heroes(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data['page'])
    await call.message.edit_text(heroes_pagination(page, HEROES_PER_PAGE),
                                 parse_mode=ParseMode.HTML,
                                 reply_markup=get_ikb_heroes_pagination(page, HEROES_PER_PAGE))
