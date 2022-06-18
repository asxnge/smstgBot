from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import bot, vip
from filters import IsAdmin
from keyboards import inline as menu
from utils import config, AdminService, Numbers, Country
from states import RentPercent, AdminActivatePercent


@vip.message_handler(state=RentPercent.percent)
async def new_rent_percent(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['percent'] = msg.text
    await msg.answer(text='Для подтверждения отправьте "+"')
    await RentPercent.next()

@vip.message_handler(state=RentPercent.confirm)
async def rent_percent_confirm(msg: types.Message, state: FSMContext):
    try:
        if msg.text.startswith("+"):
            async with state.proxy() as data:
                time = data['time']
                percent = data['percent']
            config.edit_config(str(time), percent)
            await msg.answer(text='Обновлено!', reply_markup=menu.close_markup())
            await state.finish()
        else:
            await state.finish()
            await msg.answer(text='Действие отменено!', reply_markup=menu.close_markup())
    except:
        await state.finish()
        await msg.answer(text='Ошибка', reply_markup=menu.close_markup())


@vip.message_handler(state=AdminActivatePercent.percent)
async def activate_new_percent(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            data['percent'] = msg.text
        await msg.answer(text=f'Введите "+", чтобы поставить наценку {msg.text} %')
        await AdminActivatePercent.next()
    else:
        await state.finish()
        await msg.answer(text='Действие было отменено, вводить нужно цифры')
    
@vip.message_handler(state=AdminActivatePercent.confirm)
async def activate_new_percent_2(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            country, service, percent = data['country'], data['service'], data['percent']
        new_price, price = await AdminService().update_percent_service(country, service, percent)
        if new_price != 0:
            await msg.answer(text=f"""
Успешное изменение процента!
Cервис: {Numbers().service_name(service)} | {Country().get_country_name(country)}

Новая цена: {new_price} RUB
Цена на сервисе: {price} RUB

Процент: {percent} %
""",
            reply_markup=menu.close_markup())
        else:
            await msg.answer('Попробуйте позже, возникла ошибка')
        await state.finish()
    else:
        await state.finish()
        await msg.answer("Действие отменено")
