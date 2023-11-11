import json
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from loguru import logger

from data import config, dota2
from filters import UserCommand
from keyboards.pick_helper import get_ikb_wronghero, ikb_allowed_heroes, replace_hero_cb_data, remove_hero_cb_data
from loader import dp
from services.db_commands import subscription as db_sub
from services.db_commands import users as db_users
from states import WrongHeroState
from states.pick_states import WaitForHeroesState
from utils import split_words
from utils.dotabuff import find_counter_picks, check_valid_heroes, match_hero_name
from utils.exceptions import NotEnoughHeroesToAnalyze, WrongHero, TooManyHeroesToAnalyze
from utils.misc.throttling import rate_limit


@rate_limit(1, 'pick')
@dp.message_handler(UserCommand(), text="👀 Контрпикнуть команду")
@dp.message_handler(UserCommand(), commands=['pick', 'p'])
async def command_pick(message: types.Message, state: FSMContext):
    if not await db_sub.is_user_sub(message.from_user.id):
        pick_commands_left = await db_users.get_user_max_picks_per_day(user_id=message.from_user.id)
        if pick_commands_left <= 0:
            await message.answer('🙁 Вы исчерпали лимит бесплатных пиков за сегодня.\n'
                                 'Возвращайтесь завтра или купите подписку и пользуйтесь ботом бесконечно')
            return

    if message.text == "👀 Контрпикнуть команду":
        user_heroes = []
    else:
        user_heroes = split_words(message.get_args())
    await proccess_pick_command(message, user_heroes, state)


async def proccess_pick_command(message: types.Message, heroes: list[str], state: FSMContext = None,
                                call: bool = False):
    try:
        if len(heroes) < 1:
            raise NotEnoughHeroesToAnalyze

        if len(heroes) > 5:
            raise TooManyHeroesToAnalyze

        heroes = [match_hero_name(hero) for hero in heroes]
        check_valid_heroes(heroes)
        counter_picks = find_counter_picks(heroes)
    except WrongHero as e:
        ikb = get_ikb_wronghero(str(e), heroes)
        if call:
            await message.edit_text(f"Ошибка: неверный герой ({e})\n"
                                    f"P.S. Обратите внимание, что необходимо писать название каждого героя в одном "
                                    f"слове.",
                                    reply_markup=ikb)
        else:
            await message.answer(f"Ошибка: неверный герой ({e})\n"
                                 f"P.S. Обратите внимание, что необходимо писать название каждого героя в одном слове.",
                                 reply_markup=ikb)
    except NotEnoughHeroesToAnalyze:
        await state.set_state(WaitForHeroesState.heroes)
        if call:
            await message.edit_text("Напишите имена героев, которым необходимо подобрать контр-пик:",
                                    reply_markup=ikb_allowed_heroes)
        else:
            await message.answer("Напишите имена героев, которым необходимо подобрать контр-пик:",
                                 reply_markup=ikb_allowed_heroes)
    except TooManyHeroesToAnalyze:
        if call:
            await message.edit_text("Выбрано слишком много героев для анализа. Максимум: 5")
        else:
            await message.answer("Выбрано слишком много героев для анализа. Максимум: 5")
    except Exception as e:
        logger.error(f"{message.from_user.full_name} (@{message.from_user.username}) {message.text}"
                     f" | Ошибка #001 | {e}")
        if call:
            await message.edit_text("Ошибка #001: Сообщите об ошибке администратору!!!")
        else:
            await message.answer("Ошибка #001: Сообщите об ошибке администратору!!!")
    else:
        logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) /p Success! ({heroes})")
        counter_picks = list(
            filter(lambda pick: pick[1] > 0.0, sorted(counter_picks.items(), key=lambda x: x[1], reverse=True)))

        text = await create_answer(counter_picks, heroes, message.from_user.id)
        if call:
            await message.edit_text(text, parse_mode=ParseMode.HTML)
        else:
            await message.answer(text, parse_mode=ParseMode.HTML)

        if not await db_sub.is_user_sub(message.from_user.id):
            num = await db_users.get_user_max_picks_per_day(user_id=message.from_user.id) - 1
            await db_users.update_user_max_picks_per_day(user_id=message.from_user.id, num=num)


@dp.callback_query_handler(replace_hero_cb_data.filter())
async def replace_wrong_hero_callback(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    filename = callback_data['filename']
    path = Path(f"temp/pick/{filename}")
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    path.unlink(True)
    wrong_name = data['wrong_name']
    heroes = data['heroes']

    await call.message.edit_text("Введите имя нового героя:")
    await state.update_data(wrong_name=wrong_name)
    await state.update_data(heroes=heroes)
    await state.set_state(WrongHeroState.new_name)
    await WrongHeroState.new_name.set()


@dp.message_handler(state=WrongHeroState.new_name)
async def set_new_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    wrong_name = data['wrong_name']
    heroes = data['heroes']
    replacement = message.text

    heroes = list(map(lambda x: x.replace(wrong_name, replacement), heroes))
    await proccess_pick_command(message, heroes)


@dp.callback_query_handler(remove_hero_cb_data.filter())
async def remove_wrong_hero_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    filename = callback_data['filename']
    path = Path(f"temp/pick/{filename}")
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    path.unlink(True)
    wrong_name = data['wrong_name']
    heroes = data['heroes']

    heroes.remove(wrong_name)
    await proccess_pick_command(call.message, heroes, state, call=True)


@dp.message_handler(state=WaitForHeroesState.heroes)
async def wait_for_heroes(message: types.Message, state: FSMContext):
    await state.finish()

    text = message.text.replace('/pick', '')
    if text == message.text:
        text = message.text.replace('/p', '')
    user_heroes = split_words(text)

    await proccess_pick_command(message, user_heroes, state)


async def create_answer(counter_picks: list, heroes: list, user_id: int) -> str:
    answer = ''

    picks_by_pos = [
        ['1', "Carry (pos 1)"],
        ['2', "Midlaner (pos 2)"],
        ['3', "Offlaner (pos 3)"],
        ['4', "Soft Supp (pos 4)"],
        ['5', "Hard Support (pos 5)"]
    ]

    for picks in picks_by_pos:
        best_picks = list(filter(
            lambda pick: any(pick[0] == data[1] and picks[0] in data[0] for data in dota2.heroes.values()),
            counter_picks))[:config.COUNTERPICK_NUM]
        if len(best_picks):
            answer += f"\n<i>Топ контр-пик {picks[1]}:</i>\n"
            for name, lose_rate in best_picks:
                answer += (f"<a href='https://t.me/{config.BOT_LINK[1:]}?start={match_hero_name(name)}'>{name}</a>: "
                           f"{round(lose_rate * 5, 2)}%\n")

    if len(answer):
        user_heroes = list(set(heroes))
        temp = []
        for url_name, data in dota2.heroes.items():
            if url_name in user_heroes:
                temp.append(f"<a href='https://t.me/{config.BOT_LINK[1:]}?start={url_name}'>{data[1].strip()}</a>")
        user_heroes = temp

        if not await db_sub.is_user_sub(user_id):
            picks_left = await db_users.get_user_max_picks_per_day(user_id=user_id) - 1
        else:
            picks_left = '∞'
        answer = ("<b>Выведен список контр-пиков каждой позиции в порядке убывания по эффективности</b>\n" +
                  f"\n<i><b>Контр-пики против: {', '.join(user_heroes)}</b></i>\n" +
                  answer +
                  f"\n<i>❕ У вас осталось {picks_left} бесплатных пиков за сегодня.</i>")

    return answer
