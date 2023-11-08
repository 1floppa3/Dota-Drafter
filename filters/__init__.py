from aiogram import Dispatcher

from .user_command import UserCommand
from .admin_command import AdminCommand
from .subscriber_command import SubscriberCommand


def setup(dp: Dispatcher):
    dp.filters_factory.bind(UserCommand)
    dp.filters_factory.bind(AdminCommand)
    dp.filters_factory.bind(SubscriberCommand)
