from gino import Gino
from loguru import logger

from data import config

db = Gino()


async def setup_connection():
    try:
        logger.info(f"Установка подключения PostgreSQL ({config.POSTGRE_URI})")
        await db.set_bind(config.POSTGRE_URI)
        await db.gino.create_all()
    except Exception as e:
        logger.error(f"Ошибка подключения PostgreSQL ({e})")


async def close_connection():
    bind = db.pop_bind()
    if bind:
        try:
            logger.info("Закрытие подключения PostgreSQL")
            await bind.close()
        except Exception as e:
            logger.error(f"Ошибка закрытия подключения PostgreSQL ({e})")
