from aiogram import types
from middlewares.throttling import rate_limit

from loader import vip
from filters import IsPrivate

@rate_limit(5)
@vip.message_handler(IsPrivate(), commands=['help'], state="*")
async def start_handler(msg: types.Message):
    await msg.answer(f"""
Привет {msg.from_user.id}
/start Запустить бота
/help Просмотреть эту справку
		""")
