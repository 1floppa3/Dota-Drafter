import hashlib

from aiogram import types

from config import BOT_LINK, BOT_NAME
from data.dota2_heroes import DOTA2_HEROES
from loader import dp


@dp.inline_handler()
async def inline_link(inline_query: types.InlineQuery) -> None:
    text = inline_query.query or 'echo'

    if text in DOTA2_HEROES.keys():
        link = f"https://t.me/{BOT_LINK[1:]}?start={text}"
        result_id = hashlib.md5(text.encode()).hexdigest()

        article = types.InlineQueryResultArticle(
            id=result_id,
            title=BOT_NAME,
            description=f"Отправить ссылку на информацию о герое: {text}",
            input_message_content=types.InputTextMessageContent(
                message_text=link
            )
        )
        await inline_query.answer([article], cache_time=1)

