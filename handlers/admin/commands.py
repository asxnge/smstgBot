from aiogram import types

from loader import bot, vip
from utils import config
from filters import IsAdmin
from keyboards import defaut as key


@vip.message_handler(IsAdmin(), commands=['a', 'admin'])
async def admin_handler(msg: types.Message):
    await msg.answer('Добро пожаловать в админку', reply_markup=key.admin_markup())
