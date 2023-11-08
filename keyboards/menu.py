from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import DOTA2_PATCH, BOT_ADMINS
import services.db_commands.subscription as db_sub


async def kb_main_menu(user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("👀 Контрпикнуть команду"),
        KeyboardButton(f"🔝 Мета ({DOTA2_PATCH})")
    )

    kb.add(KeyboardButton("📄 Все герои"))

    if await db_sub.is_user_sub(user_id) or str(user_id) in BOT_ADMINS:
        kb.add(KeyboardButton("[SUB] Анализ пиков команд"))

    kb.add(
        KeyboardButton("👤 Профиль"),
        KeyboardButton("🔍 Помощь")
    )
    return kb
