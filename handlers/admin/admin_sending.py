from aiogram import types
from aiogram.dispatcher import FSMContext
import time, random, os, asyncio
from datetime import datetime

from loader import vip, bot
from utils import config
from data import get_users, down_sending, down_sending_markup, sending_check
from states import EmailText, EmailPhoto
from keyboards import inline as menu, defaut as key


@vip.callback_query_handler(text='email_sending_text')
async def adm_sending_text(call: types.CallbackQuery):
    await EmailText.text.set()
    await call.message.answer('<b>Введите текст рассылки:</b>')

@vip.callback_query_handler(text='edit_down_sending')
async def edit_down_sending(call: types.CallbackQuery):
    markup = down_sending_markup()
    if markup != False:
        await call.message.answer(text='Выберите рассылку', reply_markup=markup)
    else:
        await call.message.answer(text='Нет запланированных рассылок', reply_markup=menu.close_markup())

@vip.message_handler(state=EmailText.text)
async def adm_sending_text_1(msg: types.Message, state: FSMContext):
    info = msg.parse_entities()

    async with state.proxy() as data:
        data['text'] = info

    await msg.answer(text=data['text'])
    await EmailText.next()
    await bot.send_message(chat_id=msg.from_user.id, text='Выбери дальнейшее действие', reply_markup=key.admin_sending())


@vip.message_handler(state=EmailText.action)
async def admin_sending_messages_2(msg: types.Message, state: FSMContext):
    chat_id = msg.from_user.id

    if msg.text in key.admin_sending_btn:
        if msg.text == key.admin_sending_btn[0]:  # Начать
            users = get_users()
            start_time = time.time()
            amount_message = 0
            amount_bad = 0

            async with state.proxy() as data:
                text = data['text']
            await state.finish()
            await bot.send_message(chat_id=chat_id, text=f'✅ Вы запустили рассылку', reply_markup=key.main_menu())

            for i in range(len(users)):
                try:
                    await bot.send_message(chat_id=users[i][0], text=text, reply_markup=menu.close_markup())
                    amount_message += 1
                except:
                    amount_bad += 1

            sending_time = time.time() - start_time
            await bot.send_message(chat_id=chat_id,
                                   text=f'✅ Рассылка окончена\n'
                                   f'👍 Отправлено: {amount_message}\n'
                                   f'👎 Не отправлено: {amount_bad}\n'
                                   f'🕐 Время выполнения рассылки - {sending_time} секунд')
        elif msg.text == key.admin_sending_btn[1]:
            await EmailText.next()
            await bot.send_message(chat_id=chat_id,
                                   text=f'Введите дату начала рассылке в формате: ГОД-МЕСЯЦ-ДЕНЬ ЧАСЫ:МИНУТЫ\n'
                                   f'Например 2021-04-01 15:00 - рассылка будет сделана 1 числа в 15:00')

        elif msg.text == key.admin_sending_btn[2]:
            await bot.send_message(chat_id=msg.from_user.id,  text='Рассылка отменена', reply_markup=key.main_menu())
            await state.finish()


@vip.message_handler(state=EmailText.down)
async def admin_sending_messages_3(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['date'] = msg.text

            date = datetime.fromisoformat(data['date'])

            await EmailText.next()
            await bot.send_message(chat_id=msg.from_user.id, text=f'Для подтверждения рассылки в {date} отправьте +')
    except:
        await state.finish()
        await msg.answer('Ошибка')


@vip.message_handler(state=EmailText.down_confirm)
async def admin_sending_messages_4(msg: types.Message, state: FSMContext):
    if msg.text == '+':
        async with state.proxy() as data:
            text = data['text']
            date = data['date']

            down_sending('text', text, random.randint(1111, 9999), date)

            await bot.send_message(chat_id=msg.from_user.id, text=f'Рассылка запланирована в {data["date"]}', reply_markup=key.main_menu())
    else:
        await bot.send_message(msg.from_user.id, text='Рассылка отменена', reply_markup=key.main_menu())
    await state.finish()


@vip.callback_query_handler(text='email_sending_photo')
async def adm_sending_photo(call: types.CallbackQuery):
    await EmailPhoto.photo.set()
    await bot.send_message(chat_id=call.from_user.id, text='Пришлите боту фото, только фото!')


@vip.message_handler(state=EmailPhoto.photo, content_types=['photo'])
async def email_sending_photo_1(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = random.randint(111111111, 999999999)

    await msg.photo[-1].download(f'utils/photos/{data["photo"]}.jpg')
    await msg.answer(text='Введите текст рассылки:')
    await EmailPhoto.next()


@vip.message_handler(state=EmailPhoto.text)
async def email_sending_photo_2(msg: types.Message, state: FSMContext):
    info = msg.parse_entities()
    async with state.proxy() as data:
        data['text'] = info

        with open(f'utils/photos/{data["photo"]}.jpg', 'rb') as photo:

            await msg.answer_photo(photo=photo, caption=data['text'])

    await EmailPhoto.next()
    await msg.answer(text='Выбери дальнейшее действие', reply_markup=key.admin_sending())


@vip.message_handler(state=EmailPhoto.action)
async def email_sending_photo_3(msg: types.Message, state: FSMContext):
    chat_id = msg.from_user.id
    if msg.text in key.admin_sending_btn:
        if msg.text == key.admin_sending_btn[0]:
            users = get_users()
            start_time = time.time()
            amount_message = 0
            amount_bad = 0

            async with state.proxy() as data:
                photo = data["photo"]
                text = data["text"]

            await bot.send_message(chat_id=chat_id, text=f'✅ Вы запустили рассылку', reply_markup=key.main_menu())

            await state.finish()
            for i in range(len(users)):
                try:
                    with open(file=f'./utils/photos/{photo}.jpg', mode='rb') as photos:
                        await bot.send_photo(chat_id=users[i][0], photo=photos, caption=text, reply_markup=menu.close_markup())
                    amount_message += 1
                except:
                    amount_bad += 1

            sending_time = time.time() - start_time

            await bot.send_message(chat_id=chat_id,
                                   text=f'✅ Рассылка окончена\n'
                                   f'👍 Отправлено: {amount_message}\n'
                                   f'👎 Не отправлено: {amount_bad}\n'
                                   f'🕐 Время выполнения рассылки - {sending_time} секунд')
            os.remove(f'./utils/photos/{photo}.jpg')
        elif msg.text == key.admin_sending_btn[1]:
            await EmailPhoto.next()
            await bot.send_message(chat_id=chat_id,
                                   text=f'Введите дату начала рассылке в формате: ГОД-МЕСЯЦ-ДЕНЬ ЧАСЫ:МИНУТЫ\n'
                                   f'Например 2021-04-01 15:00 - рассылка будет сделана 1 числа в 15:00')

        elif msg.text == key.admin_sending_btn[2]:
            await state.finish()
            await bot.send_message(chat_id=chat_id, text='Рассылка отменена', reply_markup=key.main_menu())
            await bot.send_message(msg.from_user.id, text='Меню админа', reply_markup=key.admin_markup())


@vip.message_handler(state=EmailPhoto.down)
async def email_sending_photo_4(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['date'] = msg.text
            date = datetime.fromisoformat(data['date'])

        await EmailPhoto.next()
        await bot.send_message(chat_id=msg.from_user.id, text=f'Для подтверждения рассылки в {date} отправьте +')
    except:
        await state.finish()
        await msg.answer('Упс, что то не так')


@vip.message_handler(state=EmailPhoto.down_confirm)
async def email_sending_photo_5(msg: types.Message, state: FSMContext):
    if msg.text == '+':
        async with state.proxy() as data:
            photo = data['photo']
            text = data['text']
            date = data['date']
            down_sending('photo', text, photo, date)

        await bot.send_message(chat_id=msg.from_user.id, text=f'Рассылка запланирована в {data["date"]}', reply_markup=key.main_menu())
    else:
        await bot.send_message(msg.from_user.id, text='Рассылка отменена', reply_markup=key.main_menu())
    await state.finish()

@vip.callback_query_handler(text = 'email_sending_update')
async def update_menu(call: types.CallbackQuery):
    users = get_users()
    await call.message.answer('Запущено обновление клавиатуры')
    amount_yes = 0
    amount_bad = 0
    for i in range(len(users)):
        try:
            await bot.send_message(users[i][0], '<b>♻️ Обновлено меню</b>', reply_markup=key.main_menu())
            amount_yes += 1
        except:
            amount_bad += 1
    await call.message.answer(f'✅ Рассылка окончена\n'
                                 f'👍 Отправлено: {amount_yes}\n'
                                 f'👎 Не отправлено: {amount_bad}\n')

async def sending_checked(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        info = sending_check()
        if info is not False:
            users = get_users()
            start_time = time.time()
            amount_message = 0
            amount_bad = 0
            if info[0] == 'text':
                for i in range(len(users)):
                    try:
                        await bot.send_message(users[i][0], info[1], reply_markup=menu.close_markup())
                        amount_message += 1
                    except Exception as e:
                        amount_bad += 1
                try:
                    await bot.send_message(chat_id=config.config("admin_owner"),text='✅ Рассылка завершена', reply_markup=key.main_menu())
                except:pass
                sending_time = time.time() - start_time
                await bot.send_message(
                            chat_id=config.config("admin_owner"),
                            text=f'✅ Рассылка окончена\n'
                                 f'👍 Отправлено: {amount_message}\n'
                                 f'👎 Не отправлено: {amount_bad}\n'
                                 f'🕐 Время выполнения рассылки - {sending_time} секунд')

            elif info[0] == 'photo':
                for i in range(len(users)):
                    try:
                        with open(f'./utils/photos/{info[2]}.jpg', 'rb') as photo:
                            await bot.send_photo(chat_id=users[i][0], photo=photo, caption=info[1], reply_markup=menu.close_markup())
                        amount_message += 1
                    except:
                        amount_bad += 1
                try:
                    await bot.send_message(chat_id=config.config("admin_owner"), text='✅ Рассылка завершена', reply_markup=key.main_menu())
                except:pass
                sending_time = time.time() - start_time
                try:
                    await bot.send_message(
                            chat_id=config.config("admin_owner"),
                            text=f'✅ Рассылка окончена\n'
                                 f'👍 Отправлено: {amount_message}\n'
                                 f'👎 Не отправлено: {amount_bad}\n'
                                 f'🕐 Время выполнения рассылки - {sending_time} секунд')
                except:pass
