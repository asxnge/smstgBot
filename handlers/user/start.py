from aiogram import types
from aiogram.dispatcher import FSMContext
from middlewares.throttling import rate_limit

from loader import bot, vip
from filters import IsPrivate
from utils import config
from data import User, first_join
from keyboards import defaut as key
from states import Captcha

@rate_limit(limit=1)
@vip.message_handler(IsPrivate(), commands=['start'], state="*")
async def start_handler(msg: types.Message, state: FSMContext):
    photo = 'https://i.imgur.com/PWIFphV.jpg'
    status, invite = await first_join(msg.from_user.id, msg.from_user.username, msg.text[7:])
    if status != False:
        await msg.answer_photo(photo=photo, 
                        caption=f'<b>Добро Пожаловать</b> {msg.from_user.full_name}\n'
							    f'<b>VIP SMS</b>  - лучшая смс активация в телеграм!',
						reply_markup=key.main_menu())
        await bot.send_message(config.config('admin_group'), f'Новый пользователь {msg.from_user.get_mention(as_html=True)} | {msg.from_user.id}')
        if invite != 0:
            await bot.send_message(invite, f'У вас новый реферал: {msg.from_user.get_mention(as_html=True)} !')
    else:
        if User(msg.from_user.id).ban == 'no':
            await msg.answer_photo(photo=photo, caption=f'{msg.from_user.full_name}, рад видеть тебя снова', reply_markup=key.main_menu())