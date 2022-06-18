import asyncio
from utils.misc import country
from aiogram import types
from aiogram.dispatcher import FSMContext
from middlewares.throttling import rate_limit

from loader import bot, vip
from data import messages as mes, get_user, delete_button, btn_info, payments_user_markup, \
    down_sending_info, del_sending, Cripto, amount_referals, User
from keyboards import defaut as key, inline as menu
from utils import config, Country, Numbers, Operator, FavoriteSerivice, SMSService, \
    RentNumber, RentBuyer, QiwiPay
from states import ShareYourBalance, QiwiKassa, AdminGiveBalance

@rate_limit(5)
@vip.callback_query_handler(state="*")
async def handler_call(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.from_user.id
    message_id = call.message.message_id

    if await get_user(chat_id) == True:
        user = User(chat_id)
        if user.ban == 'no':

            if call.data == 'to_closed':
                await bot.delete_message(chat_id, message_id)

            if call.data == 'to_menu':
                await call.message.edit_caption(
                                caption=f'<b>💳 Баланс: {user.balance} RUB</b>\n'
                                        f'<b>🌍 Выбранная страна:</b> {Country().get_country_name(user.country)}\n '
                                        f'<b>♻️ Выбранный оператор:</b> {Operator().get_operator_name(user.country, user.operator)}',
                                reply_markup=menu.sms_markup())

            if call.data == 'user_country':
                markup = Country().country_menu()
                await call.message.edit_reply_markup(reply_markup=markup)

            if call.data.split(":")[0] == 'page':
                markup = Country().country_menu(int(call.data.split(":")[1]))
                await call.message.edit_reply_markup(reply_markup=markup)

            if call.data.split(":")[0] == 'country':
                await user.up_country(call.data.split(":")[1])
                await user.up_operator('any')
                await call.message.edit_caption(
                                caption=f'<b>💳 Баланс: {user.balance} RUB</b>\n'
                                        f'<b>🌍 Выбранная страна:</b> {Country().get_country_name(call.data.split(":")[1])}\n '
                                        f'<b>♻️ Выбранный оператор:</b> {Operator().get_operator_name(call.data.split(":")[1], user.operator)}',
                                reply_markup=menu.sms_markup())

            if call.data == 'user_activate':
                markup = Numbers().service_menu(user.country)
                await call.message.edit_reply_markup(reply_markup=markup)

            if call.data.split(":")[0] == 'service_page':
                markup = Numbers().service_menu(call.data.split(":")[1], int(call.data.split(":")[2]))
                await call.message.edit_reply_markup(reply_markup=markup)

            if call.data.split(":")[0] == 'service_pages':
                markup = Numbers().service_menu(call.data.split(":")[1])

                await bot.edit_message_caption(chat_id=chat_id, message_id=message_id,
                                               caption=f'<b>💳 Баланс: {user.balance} RUB</b>\n'
                                               f'<b>🌍 Выбранная страна:</b> {Country().get_country_name(user.country)}\n'
                                               f'<b>🧿 Выбранный оператор:</b> {Operator().get_operator_name(user.country, user.operator)}',
                                               reply_markup=markup)

            if call.data == 'get_operators':
                name = Operator().get_operator_name(user.country, user.operator)
                text = f'<b>🧿 Активный оператор:</b> {name}\n<b>🌐 Выберите оператора:</b>'
                markup = Operator().operator_menu(user.country)

                await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'set_operator':
                await user.up_operator(call.data.split(":")[1])
                name = Operator().get_operator_name(user.country, call.data.split(":")[1])
                text = f'Выбран оператор: {name}'

                await call.message.edit_caption(caption=text, reply_markup=menu.close_markup())

            if call.data.split(":")[0] == 'add_favorite':
                await FavoriteSerivice().add_favorite(chat_id, call.data.split(":")[1], call.data.split(":")[2])
                markup = await Numbers().get_buy_menu(chat_id, call.data.split(":")[1], call.data.split(":")[2])

                await call.answer(text=f'Сервис: {Numbers().service_name(call.data.split(":")[2])}, успешно добавлен в избранное')
                await call.message.edit_reply_markup(reply_markup=markup)

            if call.data.split(":")[0] == 'del_favorite':
                await FavoriteSerivice().del_favorite(chat_id, call.data.split(":")[1], call.data.split(":")[2])
                markup = Numbers().get_buy_menu(chat_id, call.data.split(":")[1], call.data.split(":")[2])

                await call.answer(text=f'Сервис: {Numbers().service_name(call.data.split(":")[2])}, успешно удален из избранного')
                await call.message.edit_reply_markup(reply_markup=markup)

            if call.data == 'favorite_service':
                text = '<b>Ваши избранные номера:</b>'
                markup = await FavoriteSerivice().get_menu(chat_id)
                if markup != False:
                    await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup)
                else:
                    await call.answer('У вас нет избранных сервисов')

            if call.data.split(":")[0] == 'buy_service':
                service = Numbers().service_name(call.data.split(":")[2])
                price = await Numbers().get_service_price(call.data.split(":")[1], call.data.split(":")[2])
                text = mes.number_info.format(service=service, balance=user.balance,
                                                   country=Country().get_country_name(call.data.split(":")[1]), price=price)
                markup = await Numbers().get_buy_menu(chat_id, call.data.split(":")[1], call.data.split(":")[2])

                await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'sms_service':
                await call.message.edit_caption(caption='<b>♻️ Подождите...</b>')
                await SMSService().buy_service(bot, chat_id, call.data.split(":")[2], call.data.split(":")[1], call.data.split(":")[3])


            if call.data.split(":")[0] == 'still_number':
                info = await SMSService().get_info_sms(call.data.split(":")[3])
                await SMSService().set_status(call.data.split(":")[3], info[8], 3)
                markup = SMSService().menu_end(info[1], info[8])
                await call.message.answer(text=f'<b>🧿 Cервис:</b> {Numbers().service_name(call.data.split(":")[1])}\n'
                                          f'<b>🌏 Cтрана:</b> {Country().get_country_name(info[4])}\n'
                                          f'<b>💈 Номер:</b> <code>{info[2]}</code>\n'
                                          f'<i>Запрошен повторный код смс активации</i>',
                                        reply_markup=markup)
                await SMSService().update_wait_status(call.data.split(":")[3], 'more_code')
                await bot.delete_message(chat_id, message_id)

            if call.data.split(":")[0] == 'cancel_number':
                text = await SMSService().cancel_number(chat_id, call.data.split(":")[1], call.data.split(":")[2], call.data.split(":")[3])
                await SMSService().del_wait_sms(call.data.split(":")[1])
                await bot.delete_message(chat_id, message_id)
                await call.message.answer(text=text, reply_markup=menu.close_markup())

            if call.data.split(":")[0] == 'end_number':
                text = await SMSService().end_service(call.data.split(":")[1], call.data.split(":")[2])
                await bot.delete_message(chat_id, message_id)
                await call.message.answer(text=text, reply_markup=menu.close_markup())

            if call.data == 'user_rent':
                markup = RentNumber().get_rent_menu()
                text = mes.rent_info.format(country=Country().get_country_name(user.country))
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data == 'rent_service':
                markup = RentNumber().rent_service_menu(user.country)
                text = f'<b>🌍 Выбранная страна:</b> {Country().get_country_name(user.country)}\n<b>🧿 Выбранный оператор:</b> {Operator().get_operator_name(user.country, user.operator)}'
                await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'rent_page':
                markup = RentNumber().rent_service_menu(call.data.split(":")[1], int(call.data.split(":")[2]))
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=markup)

            if call.data.split(":")[0] == 'buy_rent':
                markup = RentNumber().rent_time_menu(call.data.split(":")[1], call.data.split(":")[2])
                text = '<b>🕐Выберите срок на который хотите арендовать номер:</b>'
                await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'rent_time':
                text, markup = await RentNumber().buy_rent_menu(call.data.split(":")[1], call.data.split(":")[2], call.data.split(":")[3])
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'rent_buy':
                info = await RentBuyer().buy_rents(chat_id, call.data.split(":")[2], call.data.split(":")[1], user.operator, call.data.split(":")[3])
                if info != 'NO_RENT':
                    if info != 'NO_BALANCE':
                        await call.message.edit_caption(caption=f'<b>📞 Успешная аренда номера!</b>\n\n'
                                                        f'<b>🛠 Cервис:</b> {Numbers().service_name(call.data.split(":")[2])}\n'
                                                        f'<b>🌍Cтрана:</b> {Country().get_country_name(call.data.split(":")[1])}\n\n'
                                                        f'<b>📲 Оператор:</b> {Operator().get_operator_name(call.data.split(":")[1], user.operator)} \n\n'
                                                        f'<b>📱 Номер:</b> +<code>{info[0]}</code>\n'
                                                        f'<b>⏱ Дата окончания:</b> {info[1]}\n\n'
                                                        f'<i>⚠️Внимание! Вы можете отменить аренду номера в течении 15 минут, если на номер не было получено SMS. Отменить номер можно в разделе «⏰Активная аренда».</i>',
                                                    reply_markup=menu.close_markup())
                    else:
                        await call.message.answer(text='Пополните баланс!')
                else:
                    await call.message.answer(text='Нет доступных номеров')

            if call.data == 'my_rent_service':
                text = '<b>📖Тут отображаются ваши арендованные номера</b>'
                markup = await RentBuyer().get_menu_my_rent(chat_id)
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'my_rent':
                msg, markup = await RentBuyer().my_rent_info(call.data.split(":")[1])
                await call.message.edit_caption(caption=msg, reply_markup=markup)

            if call.data.split(":")[0] == 'rent_cancel':
                text = await RentBuyer().cancel_rent(call.data.split(":")[1])
                await call.message.edit_caption(caption=text, reply_markup=menu.close_markup())

            if call.data == 'to_rent':
                markup = RentNumber().get_rent_menu()
                text = mes.rent_info.format(country=Country().get_country_name(user.country))
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'to_rent_service':
                markup = RentNumber().rent_service_menu(call.data.split(":")[1])
                text = f'<b>🌍 Выбранная страна:</b> {Country().get_country_name(user.country)}'
                await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'to_rent_time':
                markup = RentNumber().rent_time_menu(call.data.split(":")[1], call.data.split(":")[2])
                text = '<b>🕐Выберите срок на который хотите арендовать номер:</b>'
                await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup)

            if call.data == 'share_amount':
                await ShareYourBalance.user_id.set()
                await call.message.answer('<b>Введите id пользователя, с которым нужно поделиться</b>')

            if call.data == 'payments':
                await call.message.edit_caption(caption='<b>Выберите способ пополнения:</b>', reply_markup=menu.pay_markup())

            if call.data == 'payment_btc':
                await call.message.edit_caption(caption=mes.btc_pay, reply_markup=menu.close_markup())

            if call.data == 'payment_qiwi':
                url, code, phone = await QiwiPay().deposit_qiwi(chat_id)
                text = mes.pay_qiwi.format(number=phone, code=code)
                await call.message.edit_caption(caption=text, reply_markup=menu.pay_qiwi_markup(url))

            if call.data.split(":")[0] == 'info_btn':
                text, markup = btn_info(call.data.split(":")[1])
                await bot.delete_message(chat_id, message_id)
                await call.message.answer(text=text, reply_markup=markup)
            
            if call.data.split(":")[0] == 'del_btn':
                delete_button(call.data.split(":")[1])
                await bot.delete_message(chat_id, message_id)
                await call.message.answer(text='Успешно удалена кнопка', reply_markup=menu.close_markup())

            if call.data == 'сurs_money':
                text = Cripto().message_curs()
                await call.message.answer(text=text, reply_markup=menu.close_markup())

            if call.data == 'refferal_program':
                name = await bot.get_me()
                text = mes.refferal.format(ref_percent=config.config("ref_percent"), bot_login=name.username,
                                        user_id=chat_id, referals=await amount_referals(chat_id))
                await call.message.edit_caption(caption=text, reply_markup=menu.close_markup())

            if call.data.split(":")[0] == 'notify_me':
                await SMSService().add_notify(chat_id, call.data.split(":")[1], call.data.split(":")[2], call.data.split(":")[3])
                await call.message.edit_text(text='Отлично, когда появятся номера, мы оповестим!', reply_markup=menu.close_markup())
            
            if call.data == 'accept_agreements':
                photo = 'https://i.imgur.com/YKDmFt2.jpg'
                text = mes.start.format(full_name=call.from_user.first_name)
                await call.message.answer_photo(photo=photo, caption=text, reply_markup=key.main_menu())

            if call.data == 'our_projects':
                await call.message.edit_caption(caption='<b>Кликай по кнопкам ниже:</b>', reply_markup=menu.projects_markup())

            if call.data == 'uor_rules':
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
                await call.message.answer(text=mes.user_agreement, reply_markup=menu.close_markup())

        

