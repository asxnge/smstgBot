from data.functions.admin import get_users
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import bot, vip
from filters import IsAdmin
from data import get_user, User
from keyboards import defaut as key, inline as menu
from states import AdminSearch, AdminGiveBalance
from utils import config, Country, Operator


@vip.message_handler(state=AdminSearch.user_id)
async def admin_search(msg: types.Message, state: FSMContext):
    await state.finish()
    if msg.text.isdigit() == True:
        if await get_user(msg.text) == True:
            user = User(msg.text)
            await bot.send_message(chat_id=msg.from_user.id,
                                   text=f'<b>👤 Пользователь:</b> @{user.username}\n\n'
                                   f'<b>💳 Баланс:</b> <code>{user.balance}</code> RUB\n\n'
                                   f'<b>📲 Выбранный оператор:</b> {Operator().get_operator_name(user.country, user.operator)}\n\n'
                                   f'<b>🌏 Выбранная страна:</b> {Country().get_country_name(user.country)}\n\n'
                                   f'<b>💢 Бан:</b> <code>{user.ban}</code> (yes - значит в бане)\n\n'
                                   f'<b>🕰 Дата регистрации:</b> <code>{user.date[:10]}</code>',
                                   reply_markup=menu.admin_user_markup(msg.text))
        else:
            await msg.answer('Мы не нашли такого пользователя в базе')
    else:
        await msg.answer('Айди всегда состоит из цифр, ок?')

@vip.message_handler(state=AdminGiveBalance.amount)
async def give_amount(msg: types.Message, state: FSMContext):
    if msg.text.isdecimal():
        async with state.proxy() as data:
            data['amount'] = msg.text
        await msg.answer(text='Введите "+" для подтверждения')
        await AdminGiveBalance.next()
    else:
        await state.finish()
        await msg.answer('Ввведененное, не является числом')

@vip.message_handler(state=AdminGiveBalance.confirm)
async def give_confirm(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            await User(data['user_id']).up_balance(data['amount'])
        await msg.answer(text=f'Пользователю: @{User(data["user_id"]).username} обновлен баланс!')
    else:
        await msg.answer(text='Действие отменено')
    await state.finish()