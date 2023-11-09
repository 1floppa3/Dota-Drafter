import hashlib

from aiogram import types

from data import config, dota2
from loader import dp


@dp.inline_handler()
async def inline_link(inline_query: types.InlineQuery) -> None:
    text = inline_query.query or 'echo'

    if text in dota2.heroes.keys():
        link = f"https://t.me/{config.BOT_LINK[1:]}?start={text}"
        result_id = hashlib.md5(text.encode()).hexdigest()

        article = types.InlineQueryResultArticle(
            id=result_id,
            title=config.BOT_NAME,
            description=f"Отправить ссылку на информацию о герое: {text}",
            input_message_content=types.InputTextMessageContent(
                message_text=link
            )
        )
        await inline_query.answer([article], cache_time=1)
