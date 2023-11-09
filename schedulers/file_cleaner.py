import shutil
from pathlib import Path

from utils.notify_admins import log_to_admins


async def daily_file_cleaning(dp):
    path = Path("temp/")
    shutil.rmtree(path, True)
    await log_to_admins(dp, "Ежедневная чистка временных файлов выполнена.")
