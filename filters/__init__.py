from aiogram import Dispatcher

from .filters import IsGroup
from .filters import IsPrivate
from .filters import IsAdmin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsAdmin)
