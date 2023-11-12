import hashlib

from aiogram import types
from aiogram.types import ParseMode

from data import config, dota2
from loader import dp
from utils.dotabuff import match_hero_name


@dp.inline_handler()
async def inline_link(inline_query: types.InlineQuery) -> None:
    text = inline_query.query or 'echo'

    values_list = []
    for names in list(dota2.heroes.values())[1:]:
        for name in names:
            values_list.append(name)
    if text in list(dota2.heroes.keys()) + values_list:
        url_name = match_hero_name(text)
        if url_name not in dota2.heroes.keys():
            return

        link = f"https://t.me/{config.BOT_LINK[1:]}?start={url_name}"
        result_id = hashlib.md5(url_name.encode()).hexdigest()

        article = types.InlineQueryResultArticle(
            id=result_id,
            title=config.BOT_NAME,
            description=f"Отправить ссылку на информацию о герое: {url_name}",
            input_message_content=types.InputTextMessageContent(
                message_text=f"Инфо о герое: <a href='{link}'>{dota2.heroes[url_name][1]}</a>",
                parse_mode=ParseMode.HTML
            ),
            thumb_url=f"https://dota2protracker.com/static/hero_images_jpg_res/{url_name.replace('-', '_')}_lg.jpg"
        )
        await inline_query.answer([article], cache_time=1)
