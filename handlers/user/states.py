from utils.misc import operator
from aiogram import types
from aiogram.dispatcher import FSMContext
import os

from loader import bot, vip
from data import messages, get_user, User
from keyboards import defaut as key, inline as menu
from states import Captcha, ShareYourBalance, QiwiKassa
from utils import config



@vip.message_handler(state=ShareYourBalance.user_id)
async def share_your_balance(msg: types.Message, state: FSMContext):
    if await get_user(msg.text) == True:
        if msg.text != msg.from_user.id:
            async with state.proxy() as data:
                data['user_id'] = msg.text
            await msg.answer(f'Введите сумму перевода (пользователь: @{User(msg.text).username})')
            await ShareYourBalance.next()
        else:
            await msg.answer(text='Нельзя перевести самому себе!')
    else:
        await state.finish()
        await msg.answer('💢 Не нашли такого пользователя в нашей базе')


@vip.message_handler(state=ShareYourBalance.amount)
async def share_your_balance_1(msg: types.Message, state: FSMContext):
    try:
        if float(msg.text) <= float(User(msg.from_user.id).balance):
            async with state.proxy() as data:
                data['amount'] = msg.text
            await msg.answer('Подтвердите перевод, отправьте "+"')
            await ShareYourBalance.next()
        else:
            await state.finish()
            await msg.answer('💢 У вас на балансе нет данной суммы!')
    except:
        await state.finish()
        await msg.answer('💢 Сумма должна состоять из цифр!')


@vip.message_handler(state=ShareYourBalance.confirm)
async def share_your_balance_2(msg: types.Message, state: FSMContext):
    if msg.text == '+':
        async with state.proxy() as data:
            user_id = data['user_id']
            amount = data['amount']
        await User(user_id).update_balance(amount)
        await User(msg.from_user.id).update_balance(-float(amount))
        await msg.answer(f'🧿 Успешный перевод баланса!\n'
                         f'Пользователь: @{User(user_id).username}\n'
                         f'Cумма: {amount} RUB', reply_markup=menu.close_markup())
        await bot.send_message(chat_id=user_id,
                                text=f'С вами поделились балансом!Капнуло + {amount} RUB')
    else:
        await msg.answer('Действие отменено!')
    await state.finish()

