from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils import config


class IsGroup(BoundFilter):

    async def check(self, message: types.Message):
        return message.chat.type in (types.ChatType.GROUP,
                                     types.ChatType.SUPERGROUP)


class IsPrivate(BoundFilter):

    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return str(message.from_user.id) in config.config("admin_owner")
