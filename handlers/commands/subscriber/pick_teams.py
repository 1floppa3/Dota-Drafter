from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InputFile
from loguru import logger

from data.dota2_heroes import DOTA2_HEROES
from filters import UserCommand, SubscriberCommand
from loader import dp
from states import TeamPickState
from utils import split_words
from utils.dotabuff import match_hero_name, check_valid_heroes, determine_match_winner
from utils.exceptions import NotEnoughHeroesToAnalyze, TooManyHeroesToAnalyze, WrongHero
from utils.misc.throttling import rate_limit


@rate_limit(1, 'pick_teams')
@dp.message_handler(UserCommand(), SubscriberCommand(), text="[SUB] Анализ пиков команд")
@dp.message_handler(UserCommand(), SubscriberCommand(), commands=['pick_teams', 'pt'])
async def command_pick_teams(message: types.Message, state: FSMContext):
    await message.answer('Введите пик первой команды:')
    await state.set_state(TeamPickState.first_team)


@dp.message_handler(state=TeamPickState.first_team)
async def set_first_team(message: types.Message, state: FSMContext):
    await heroes_handler(message, state, True)


@dp.message_handler(state=TeamPickState.second_team)
async def set_second_team(message: types.Message, state: FSMContext):
    await heroes_handler(message, state, False)


async def heroes_handler(message: types.Message, state: FSMContext, first_step: bool):
    heroes = split_words(message.text)

    try:
        if len(heroes) < 5:
            raise NotEnoughHeroesToAnalyze

        if len(heroes) > 5:
            raise TooManyHeroesToAnalyze

        heroes = [match_hero_name(hero) for hero in heroes]
        check_valid_heroes(heroes)
    except NotEnoughHeroesToAnalyze:
        await message.answer("Указано недостаточно героев для "
                             f"{'первой' if first_step else 'второй'} команды. Необходимо: 5")
        await state.finish()
    except TooManyHeroesToAnalyze:
        await message.answer("Указано слишком много героев для "
                             f"{'первой' if first_step else 'второй'} команды. Необходимо: 5")
        await state.finish()
    except WrongHero as e:
        await message.answer(f"Ошибка: неверный герой ({e})\n"
                             f"P.S. Обратите внимание, что необходимо писать название каждого героя в одном слове.")
        await state.finish()
    else:
        if first_step:
            await state.update_data(first_team=heroes)
            await state.set_state(TeamPickState.second_team)
            await message.answer('Введите пик второй команды:')
        else:
            data = await state.get_data()
            await state.finish()
            first_team = data['first_team']
            second_team = heroes

            if len(set(first_team) & set(second_team)):
                await message.answer("Обнаружено пересечение героев в Команде #1 и Команде #2")
                return

            try:
                sum_rate = determine_match_winner(first_team, second_team)
            except Exception as e:
                logger.error(f"{message.from_user.full_name} (@{message.from_user.username}) {message.text}"
                             f" | Ошибка #002 | {e}")
                await message.answer("Ошибка #002: Сообщите об ошибке администратору!!!")
            else:
                logger.info(f"{message.from_user.full_name} (@{message.from_user.username}) /pt Success! "
                            f"({first_team} vs {second_team})")

                temp1 = []
                temp2 = []
                for url_name, data in DOTA2_HEROES.items():
                    if url_name in first_team:
                        temp1.append(f"<code>{data[1].strip()}</code>")
                    if url_name in second_team:
                        temp2.append(f"<code>{data[1].strip()}</code>")
                first_team = temp1
                second_team = temp2

                photo = InputFile(path_or_bytesio='media/team1vsteam2.jpg')
                await message.answer_photo(photo, "<b>Анализ матчапа...</b>\n\n"
                                                  f"<b>Команда #1:</b> {', '.join(first_team)}\n"
                                                  f"<b>Команда #2:</b> {', '.join(second_team)}\n\n"
                                                  f"<i>Победитель по драфту: "
                                                  f"{'Команда #1' if sum_rate > 0 else 'Команда #2'}\n"
                                                  f"Перевес составляет <b>{abs(round(sum_rate, 2))}%</b></i>\n\n"
                                                  f"<b><u>ВНИМАНИЕ: Данный анализ основывается на сухой статистике "
                                                  f"и не берёт во внимание формы команд</u></b>",
                                           parse_mode=ParseMode.HTML)
