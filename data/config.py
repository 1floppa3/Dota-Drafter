import os

from dotenv import load_dotenv

from data import dota2

load_dotenv()

# General
BOT_NAME = "Dota Drafter"
BOT_VERSION = "3.0"
API_TOKEN = os.getenv("API_TOKEN")

# Admins
GROUP_TO_LOG = "-1001959563681"  # group to log <group id>
BOT_ADMINS = [
    '408695718',  # FAUST
    '509056798'  # floppa
]

# Links
CHANNEL_LINK = "@dotadrafter"
BOT_LINK = "@testfloppa13bot"  # TODO поменять в проде
HERO_NAMES_URL_LINK = "https://telegra.ph/Aliasy-k-nazvaniyam-geroev-DOTA-DRAFTER-11-03"

# Misc
SUBSCRIBER_CHECK = {
    "DotaDrafter канал": ["-1001956515523", "https://t.me/dotadrafter"]  # Bot need to be admin in the channel/group
}
BOT_COMMANDS = {
    'start': 'Перезапуск бота',
    'help': 'Помощь',
    'profile': 'Профиль',
    'pick': 'Контрпикнуть команду',
    'meta': f'Мета ({dota2.patch})',
    'heroes': 'Список героев',
    'sub': 'Инфо о подписке'
}
HEROES_PER_PAGE = 25  # Heroes per page on '/heroes' command
COUNTERPICK_NUM = 7  # Count of counterpicks of each role on '/pick' command
PICKS_PER_DAY = 5  # Maximum picks per day for average user
WINRATE_TOP_NUM = 10  # Count of heroes in Winrate meta
FREQUENCY_TOP_NUM = 10  # Count of heroes in Frequency meta

# Subscription
SUBSCRIBTION_COST_RUB = 199
SUBSCRIBTION_DAYS = 30
SUBSCRIBTION_COST_MESSAGE = f"{SUBSCRIBTION_COST_RUB}₽/{SUBSCRIBTION_DAYS}дн"
PAYOK_SHOP_ID = "9101"
PAYOK_SHOP_KEY = os.getenv('PAYOK_SHOP_KEY')  # TODO добавить в енв в проде
PAYOK_API_ID = "4606"
PAYOK_API_KEY = os.getenv('PAYOK_API_KEY')  # TODO добавить в енв в проде
# TODO сразу после прода сделать скипнуть 10 индексов в БД (чтобы не было конфликтов с payok)

# Database
DATABASE = {
    "NAME": os.getenv('DB_NAME'),
    "USER": os.getenv('DB_USER'),
    "PASSWORD": os.getenv('DB_PASSWORD'),
    "HOST": os.getenv('DB_HOST')

}

POSTGRE_URI = f"postgresql://{DATABASE['USER']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}/{DATABASE['NAME']}"
