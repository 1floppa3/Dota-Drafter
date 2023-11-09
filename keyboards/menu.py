from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import services.db_commands.subscription as db_sub
from data import config, dota2


async def kb_main_menu(user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True, input_field_placeholder=config.BOT_NAME)

    row = [KeyboardButton("👀 Контрпикнуть команду")]
    if await db_sub.is_user_sub(user_id) or str(user_id) in config.BOT_ADMINS:
        row.append(KeyboardButton("[SUB] Анализ пиков команд"))
    kb.add(*row)

    kb.add(
        KeyboardButton("📄 Все герои"),
        KeyboardButton(f"🔝 Мета ({dota2.patch})")
    )

    kb.add(
        KeyboardButton("👤 Профиль"),
        KeyboardButton("💵 Подписка"),
        KeyboardButton("🔍 Помощь")
    )
    return kb
