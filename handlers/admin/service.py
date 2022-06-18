from aiogram import types
from aiogram.dispatcher import FSMContext
from random import randint

from loader import vip, bot
from states import SMSHubAPI, SMSActivateAPI
from keyboards import inline as menu
from utils import config

@vip.callback_query_handler(text='edit_api_hub')
async def admin_service_hub(call: types.CallbackQuery):
    await SMSHubAPI.api.set()
    await call.message.answer('Введите новое API SmsHUB')

@vip.message_handler(state=SMSHubAPI.api)
async def admin_hub_api(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['api'] = msg.text
    await msg.answer(text='Отправьте "+", для подтверждения')
    await SMSHubAPI.next()

@vip.message_handler(state=SMSHubAPI.confirm)
async def admin_hub_api_two(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            api = data['api']
        config.edit_config('api_smshub', api)
        await msg.answer('Успешно изменено API SMSHub')
    else:
        await msg.answer('Действие отменено!')
    await state.finish()

@vip.callback_query_handler(text='edit_api_activate')
async def admin_service_activate(call: types.CallbackQuery):
    await SMSActivateAPI.api.set()
    await call.message.answer('Введите новое API SMS Activate')

@vip.message_handler(state=SMSActivateAPI.api)
async def admin_activate_api(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['api'] = msg.text
    await msg.answer(text='Отправьте "+", для подтверждения')
    await SMSActivateAPI.next()

@vip.message_handler(state=SMSActivateAPI.confirm)
async def admin_activate_api_two(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            api = data['api']
        config.edit_config('api_smsactivate', api)
        await msg.answer('Успешно изменено API SMS Activate')
    else:
        await msg.answer('Действие отменено!')
    await state.finish()