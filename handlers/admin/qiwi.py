from aiogram import types
from aiogram.dispatcher import FSMContext
from random import randint

from loader import vip, bot
from states import EditQiwiNumber, EditQiwiToken, EditSecretQiwi
from keyboards import inline as menu
from utils import config

@vip.callback_query_handler(text='edit_qiwi_token')
async def admin_qiwi(call: types.CallbackQuery):
    await EditQiwiToken.api.set()
    await call.message.answer('Введите новый QiwiTOken')

@vip.message_handler(state=EditQiwiToken.api)
async def admin_qiwitoken(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['api'] = msg.text
    await msg.answer(text='Отправьте "+", для подтверждения')
    await EditQiwiToken.next()

@vip.message_handler(state=EditQiwiToken.confirm)
async def admin_qiwitoken_two(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            api = data['api']
        config.edit_config('qiwi_token', api)
        await msg.answer('Успешно изменен QiwiTOken')
    else:
        await msg.answer('Действие отменено!')
    await state.finish()

@vip.callback_query_handler(text='edit_qiwi_number')
async def admin_qiwinumber(call: types.CallbackQuery):
    await EditQiwiNumber.number.set()
    await call.message.answer('Введите новый QIWI номер')

@vip.message_handler(state=EditQiwiNumber.number)
async def admin_qiwinumber_1(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = msg.text
    await msg.answer(text='Отправьте "+", для подтверждения')
    await EditQiwiNumber.next()

@vip.message_handler(state=EditQiwiNumber.confirm)
async def admin_qiwinumber_two(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            api = data['number']
        config.edit_config('qiwi_number', api)
        await msg.answer('Успешно изменен QIWI номер')
    else:
        await msg.answer('Действие отменено!')
    await state.finish()

@vip.callback_query_handler(text='edit_secret_key')
async def adm_qiwi_keys(call: types.CallbackQuery):
    await EditSecretQiwi.key.set()
    await call.message.answer('Введите новый QiwiTOken')

@vip.message_handler(state=EditSecretQiwi.key)
async def admin_qiwi_key_1(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['key'] = msg.text
    await msg.answer(text='Отправьте "+", для подтверждения')
    await EditQiwiToken.next()

@vip.message_handler(state=EditSecretQiwi.confirm)
async def admin_qiwikey_two(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            api = data['key']
        config.edit_config('qiwi_key', api)
        await msg.answer('Успешно изменен QiwiTOken')
    else:
        await msg.answer('Действие отменено!')
    await state.finish()