from aiogram import types
from pyqiwi import Wallet
import asyncio

from loader import bot, vip
from filters import IsAdmin
from data import admin_stats
from keyboards import defaut as key, inline as menu
from utils import HUB, Activate, config, RentBuyer
from states import AdminSearch


@vip.message_handler(IsAdmin(), text=key.admin_button[0])
async def stats_admin(msg: types.Message):
    await msg.answer(text=admin_stats(), reply_markup=menu.admin_stats_markup())

@vip.message_handler(IsAdmin(), text=key.admin_button[2])
async def admin_message_1(msg: types.Message):
    await msg.answer('Вы перешли в настройки бота:', reply_markup=key.admin_settings())

@vip.message_handler(IsAdmin(), text=key.admin_button[3])
async def admin_message(msg: types.Message):
    await AdminSearch.user_id.set()
    await msg.answer('Введите айди пользователя:')

@vip.message_handler(IsAdmin(), text=key.admin_button[4])
async def admin_back(msg: types.Message):
    await msg.answer('Вы вернулись в главное меню', reply_markup=key.main_menu())

@vip.message_handler(IsAdmin(), text=key.admin_button[1])
async def admin_mail(msg: types.Message):
    await msg.answer('Выберите тип рассылки:', reply_markup=menu.admin_sending())

@vip.message_handler(IsAdmin(), text=key.admin_settings_btn[1])
async def admin_buttons(msg: types.Message):
    await msg.answer('Выберите тип рассылки:', reply_markup=menu.admin_btn_markup())

@vip.message_handler(IsAdmin(), text=key.admin_settings_btn[3])
async def admin_service(msg: types.Message):
    text = f"""
<b>Баланс SMS-HUB:</b> {await HUB().get_balance()} RUB
<b>Баланс SMS-Activate:</b> {await Activate().get_balance()} RUB

<b>API SMS-HUB:</b> {config.config('api_smshub')}
<b>API SMS-Activate:</b> {config.config('api_smsactivate')}
    """
    await msg.answer(text=text, reply_markup=menu.admin_service_markup())

@vip.message_handler(text=key.admin_settings_btn[0])
async def admin_qiwi(msg: types.Message):
    api = Wallet(token=config.config('qiwi_token'), number=config.config('qiwi_number'))
    text = f"""
<b>Номер:</b> {config.config('qiwi_number')}
<b>Токен:</b> {config.config('qiwi_token')}
<b>Баланс:</b> {api.balance()} RUB


<b>Cекрет ключ:</b> {config.config('qiwi_key')}
    """
    await msg.answer(text=text, reply_markup=menu.admin_qiwi_markup())

@vip.message_handler(IsAdmin(), text=key.admin_settings_btn[2])
async def admin_rent(msg: types.Message):
    markup = await RentBuyer().admin_rent_menu()
    if markup != False:
        await msg.answer(text='Нажмите чтобы просмотреть', reply_markup=markup)
    else:
        await msg.answer(text='Нет активных аренд', reply_markup=menu.close_markup())

@vip.message_handler(IsAdmin(), text=key.admin_settings_btn[4])
async def admin_percent_edit(msg: types.Message):
    await msg.answer(text='Выберите где редачить наценку', reply_markup=menu.adm_percent_markup())


