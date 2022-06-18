from aiogram import types
from aiogram.dispatcher import FSMContext
import asyncio

from loader import bot, vip
from filters import IsAdmin
from data import admin_marg, functions as func, User, payments_user_markup
from keyboards import inline as menu
import states
from utils import RentBuyer, AdminRent, AdminService, Country, Numbers, Activate
from states import RentPercent, AdminActivatePercent, AdminGiveBalance


@vip.callback_query_handler(text_startswith='adm_rent_info:')
async def admin_info_rent(call: types.CallbackQuery):
    text, markup = await RentBuyer().admin_rent_info(call.data.split(":")[1])
    await call.message.edit_text(text=text, reply_markup=markup)

@vip.callback_query_handler(text_startswith='adm_del_rent:')
async def admin_rent_del(call: types.CallbackQuery):
    text = await RentBuyer().admin_delete_rent(call.data.split(":")[1])
    await call.message.edit_text(text=text, reply_markup=menu.close_markup())

@vip.callback_query_handler(IsAdmin(), text='admin_profit')
async def admin_profit(call: types.CallbackQuery):
    await call.message.edit_text(text=admin_marg(), reply_markup=menu.close_markup())

@vip.callback_query_handler(IsAdmin(), text='edit_percent_rent')
async def rent_percent(call: types.CallbackQuery):
    markup = AdminRent().adm_rent_menu()
    await call.message.edit_text('Выбирите время аренды, для которой изменить наценку', reply_markup=markup)

@vip.callback_query_handler(IsAdmin(), text_startswith='adm_rent_edit:')
async def percent_time_rent(call: types.CallbackQuery, state: FSMContext):
    if call.data.split(":")[1] == 4:
        time = 'rent_percent_4h'
    elif call.data.split(":")[1] == 12:
        time = 'rent_percent_12h'
    elif call.data.split(":")[1] == 24:
        time = 'rent_percent_24h'
    elif call.data.split(":")[1] == 24:
        time = 'rent_percent_72h'
    elif call.data.split(":")[1] == 24:
        time = 'rent_percent_168h'
    else:
        time = 'rent_percent_336h'

    await RentPercent.percent.set()
    async with state.proxy() as data:
        data['time'] = time
    await call.message.answer(text=f'Введите новый процент для {call.data.split(":")[1]} ч')

@vip.callback_query_handler(IsAdmin(), text='edit_percent_act')
async def edit_activate_country(call: types.CallbackQuery):
    markup = AdminService().country_adm_menu()
    text = 'Выберите страну для редактирования цен в ней'
    await call.message.answer(text=text, reply_markup=markup)

@vip.callback_query_handler(IsAdmin(), text_startswith='adm_page:')
async def edit_activate_country_2(call: types.CallbackQuery):
    markup = AdminService().country_adm_menu(int(call.data.split(":")[1]))
    text = 'Выберите страну для редактирования цен в ней'
    await call.message.edit_text(text=text, reply_markup=markup)

@vip.callback_query_handler(IsAdmin(), text_startswith='adm_country:')
async def edit_activate_service(call: types.CallbackQuery):
    country = call.data.split(":")[1]
    text = f'Страна: {Country().get_country_name(country)}\nВыберите сервис для редактирования его цены:'
    markup = AdminService().service_menu(country)
    await call.message.edit_text(text=text, reply_markup=markup)

@vip.callback_query_handler(IsAdmin(), text_startswith='adm_service_page:')
async def edit_activate_service_2(call: types.CallbackQuery):
    country = call.data.split(":")[1]
    text = f'Страна: {Country().get_country_name(country)}\nВыберите сервис для редактирования его цены:'
    markup = AdminService().service_menu(country, int(call.data.split(":")[2]))
    await call.message.edit_text(text=text, reply_markup=markup)

@vip.callback_query_handler(IsAdmin(), text_startswith='adm_service:')
async def edit_activate_percent(call: types.CallbackQuery, state: FSMContext):
    percent = await AdminService().get_percent(call.data.split(":")[1], call.data.split(":")[2])
    await AdminActivatePercent.percent.set()
    async with state.proxy() as data:
        data['country'] = call.data.split(":")[1]
        data['service'] = call.data.split(":")[2]
    await call.message.edit_text(text=f"""
Cервис: {Numbers().service_name(call.data.split(":")[2])}
Страна: {Country().get_country_name(call.data.split(":")[1])}
Цена Activate: {await Activate().get_price(call.data.split(":")[1], call.data.split(":")[2])} RUB
Нынешний процент: {percent} %

Введите новый процент для этого сервиса:
""")

@vip.callback_query_handler(IsAdmin(), text_startswith='admin_ban:')
async def admin_ban(call: types.CallbackQuery):
    await User(call.data.split(":")[1]).up_ban("yes")
    await call.message.answer(text=f'Пользователь: @{User(call.data.split(":")[1]).username} забанен')

@vip.callback_query_handler(IsAdmin(), text_startswith='admin_unban:')
async def admin_unban(call: types.CallbackQuery):
    await User(call.data.split(":")[1]).up_ban("no")
    await call.message.answer(text=f'Пользователь: @{User(call.data.split(":")[1]).username} разбанен')

@vip.callback_query_handler(IsAdmin(), text_startswith='give_balance:')
async def give_amount_admin(call: types.CallbackQuery, state: FSMContext):
    await AdminGiveBalance.amount.set()
    async with state.proxy() as data:
        data['user_id'] = call.data.split(":")[1]
    await call.message.answer(text='Введите сумму изменения баланса:')

@vip.callback_query_handler(IsAdmin(), text_startswith='admin_payments:')
async def admin_pays(call: types.CallbackQuery):
    info = payments_user_markup(call.data.split(":")[1])
    if info != False:
        await call.message.edit_reply_markup(reply_markup=info)
    else:
        await call.message.answer('У пользователя нет пополнений')

@vip.callback_query_handler(IsAdmin(), text_startswith='info_sending:')
async def admin_info_sending(call: types.CallbackQuery):
    text, markup = func.down_sending_info(call.data.split(":")[1])
    await call.message.edit_text(text=text, reply_markup=markup)

@vip.callback_query_handler(IsAdmin(), text_startswith='del_sending:')
async def admin_del_sending(call: types.CallbackQuery):
    func.del_sending(call.data.split(':')[1])
    await call.message.edit_text(text='Успешно удалено', reply_markup=menu.close_markup())