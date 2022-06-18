from aiogram import Dispatcher

from loader import vip
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    vip.middleware.setup(ThrottlingMiddleware())