from middlewares.throttling import rate_limit
from aiogram import types
import re

from loader import bot, vip
from filters import IsPrivate
from keyboards import inline as menu, defaut as key
from data import messages, User, get_user, btn_menu_list, info_buttons
from utils import config, Country, Operator, BTCPayment


@rate_limit(1)
@vip.message_handler(IsPrivate(), content_types=['text'], state="*")
async def message_handler(msg: types.Message):
    chat_id = msg.from_user.id

    if await get_user(chat_id):
        user = User(chat_id)
        if user.ban == 'no':

            if msg.text in btn_menu_list():
                info = info_buttons(msg.text)
                with open(f'utils/photos/{info[2]}.jpg', 'rb') as photo:
                    await bot.send_photo(chat_id=chat_id, photo=photo, caption=info[1], reply_markup=menu.close_markup())

            elif msg.text == key.store_buttons[0]:
                photo = 'https://i.imgur.com/PWIFphV.jpg'
                await msg.answer_photo(photo=photo,
                                caption=f'<b>💳 Баланс: {user.balance} RUB</b>\n'
                                        f'<b>🌍 Выбранная страна:</b> {Country().get_country_name(user.country)}\n '
                                        f'<b>♻️ Выбранный оператор:</b> {Operator().get_operator_name(user.country, user.operator)}',
                                reply_markup=menu.sms_markup())

            elif msg.text == key.store_buttons[1]:
                photo = 'https://i.imgur.com/PWIFphV.jpg'
                text = messages.cabinet.format(user_id=chat_id,
                                               full_name=msg.from_user.get_mention(
                                                   as_html=True),
                                               operator=Operator().get_operator_name(user.country, user.operator),
                                               country=Country().get_country_name(user.country), balance=user.balance,
                                               data=user.get_days())
                await msg.answer_photo(photo=photo, caption=text, reply_markup=menu.cabinet_markup())

            elif msg.text == key.store_buttons[2]:
                photo = 'https://i.imgur.com/PWIFphV.jpg'
                text = '<b>Информация о наших проектах:</b>'
                await msg.answer_photo(photo=photo, caption=text, reply_markup=menu.information_markup())

            elif re.search(r'BTC_CHANGE_BOT\?start=', msg.text) or re.search(r'Chatex_bot\?start=', msg.text) \
                or re.search(r'ETH_CHANGE_BOT\?start=', msg.text):
                await msg.answer('<b>♻️ Секундочку...</b>')
                await BTCPayment().receipt_parser(bot, chat_id, msg.text)

            else:
                await msg.answer('Я не понимаю тебя', reply_markup=key.main_menu())
