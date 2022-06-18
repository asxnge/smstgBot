from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_user_markup(user_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Изменить баланс',
                                     callback_data=f'give_balance:{user_id}'),
            ],
            [
                InlineKeyboardButton(
                    text='Забанить', callback_data=f'admin_ban:{user_id}'),
                InlineKeyboardButton(
                    text='Разбанить', callback_data=f'admin_unban:{user_id}'),
            ],
            [
                InlineKeyboardButton(
                    text='Пополнения', callback_data=f'admin_payments:{user_id}')
            ]
        ]
    )
    return markup


def admin_sending():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✔️ Рассылка(только текст)', callback_data='email_sending_text'),
                InlineKeyboardButton(
                    text='✔️ Рассылка(текст + фото)', callback_data='email_sending_photo'),
            ],
            [
                InlineKeyboardButton(
                    text='Управление заплан. рассылками', callback_data='edit_down_sending'),
            ],
            [
                InlineKeyboardButton(text='Обновить меню',
                                     callback_data='email_sending_update'),
            ],
            [
                InlineKeyboardButton(
                    text='💢 Отмена', callback_data='to_closed'),
            ]
        ]
    )

    return markup

def admin_btn_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = 'Добавить кнопку', 
                                    callback_data = 'admin_button_add'),
			],
			[
				InlineKeyboardButton(text = 'Активные кнопки', 
                                    callback_data = 'admin_button_act'),
			],
		]
	)

	return markup

def admin_service_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = 'ИЗменить API | HUB', 
                                    callback_data = 'edit_api_hub'),
			],
			[
				InlineKeyboardButton(text = 'ИЗменить API | Activate', 
                                    callback_data = 'edit_api_activate'),
			],
		]
	)

	return markup

def admin_qiwi_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = 'ИЗменить | Token', 
                                    callback_data = 'edit_qiwi_token'),
                InlineKeyboardButton(text = 'ИЗменить | Номер', 
                                    callback_data = 'edit_qiwi_number'),
			],
			[
				InlineKeyboardButton(text = 'ИЗменить | Secret key', 
                                    callback_data = 'edit_secret_key'),
			],
		]
	)

	return markup

def admin_stats_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = 'Прибыль', 
                                    callback_data = 'admin_profit'),
			],
			[
				InlineKeyboardButton(text='💢 Отмена', 
                                    callback_data='to_closed'),
			]
		]
	)

	return markup

def adm_percent_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Активация', callback_data='edit_percent_act'),
                InlineKeyboardButton(
                    text='Аренда', callback_data='edit_percent_rent')
            ],
            [
                InlineKeyboardButton(
                    text='♨️ Закрыть', callback_data='to_closed')
            ]
        ]
    )

    return markup

