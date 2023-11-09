from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .dotabuff_parser import daily_dotabuff_parser
from .file_cleaner import daily_file_cleaning
from .picks_distribution import daily_picks_distribution


def setup(dp: Dispatcher):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(daily_dotabuff_parser, 'cron', hour=00, minute=0, args=[dp])
    scheduler.add_job(daily_picks_distribution, 'cron', hour=00, minute=0, args=[dp])
    scheduler.add_job(daily_file_cleaning, 'cron', hour=00, minute=0, args=[dp])
    scheduler.start()
