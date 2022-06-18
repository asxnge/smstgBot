from os import stat
from aiogram import types
from aiogram.dispatcher import FSMContext
from random import randint

from loader import vip, bot
from data import buttons_markup, add_button
from states import ButtonsAdd
from keyboards import inline as menu


@vip.callback_query_handler(text='admin_button_act')
async def admin_active_btn(call: types.CallbackQuery):
    info = buttons_markup()
    if info != False:
        await call.message.answer(text='Выберите кнопку', reply_markup=info)
    else:
        await call.message.answer(text='Нет активных кнопок!', reply_markup=menu.close_markup())

@vip.callback_query_handler(text='admin_button_add')
async def admin_btn_add(call: types.CallbackQuery, state: FSMContext):
    await ButtonsAdd.name.set()
    await call.message.answer(text='<b>Введите название новой кнопки:</b>')

@vip.message_handler(state=ButtonsAdd.name)
async def admin_btn_add_1(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await msg.answer(text='<b>Введите текст кнопки:</b>')
    await ButtonsAdd.next()

@vip.message_handler(state=ButtonsAdd.text)
async def admin_btn_add_2(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = msg.text
    await msg.answer(text='Отправьте фото кнопки:')
    await ButtonsAdd.next()

@vip.message_handler(state=ButtonsAdd.photo, content_types=['photo'])
async def admin_buttons_add_photo(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = randint(1111, 9999)
    photo = data['photo']

    await msg.photo[-1].download(f'utils/photos/{photo}.jpg')
    with open(f'utils/photos/{photo}.jpg', 'rb') as photo:
        await msg.answer_photo(photo=photo, caption=data['text'])

    await msg.answer(text='Для создания отправьте "+"')
    await ButtonsAdd.next()

@vip.message_handler(state=ButtonsAdd.confirm)
async def admin_btn_add_confirm(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            add_button(data['name'], data['text'], data['photo'])

        await msg.answer(text='Кнопка успешно создана!', reply_markup=menu.close_markup())
        await state.finish()
    else:
        await state.finish()
        await msg.answer(text='Создание кнопки отменено!')


