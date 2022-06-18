from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import config


def cabinet_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='💳 Пополнить баланс', callback_data='payments'),
                InlineKeyboardButton(
                    text='👮🏻‍♀️ Реферальна программа', callback_data='refferal_program'),
            ],
            [
                InlineKeyboardButton(
                    text='🧬 Поделиться балансом', callback_data='share_amount')
            ],
        ]
    )

    return markup


def sms_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='📨 Активация', callback_data='user_activate'),
                InlineKeyboardButton(
                    text='⏰ Аренда', callback_data='user_rent')
            ],
            [
                InlineKeyboardButton(
                    text='🌏 Страна/Оператор', callback_data='user_country'),
                InlineKeyboardButton(
                    text='⭐️ Избранное', callback_data='favorite_service')
            ],
            [
                InlineKeyboardButton(
                    text='💢 Закрыть', callback_data='to_closed')
            ]
        ]
    )

    return markup


def pay_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='💳 Qiwi | Card', callback_data='payment_qiwi'),
                InlineKeyboardButton(
                    text='💳 BTC/ETH Banker | Chatex', callback_data='payment_btc')
            ],
            [
                InlineKeyboardButton(
                    text='💢 Закрыть', callback_data='to_closed')
            ]
        ]
    )

    return markup


def information_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🧑🏻‍🔧 Разработчик', url='https://t.me/ZyzSoon')
            ],
            [
                InlineKeyboardButton(
                    text='🧑🏻‍🔧 Поддержка', url=f'https://t.me/{config.config("support_link")}'),
                InlineKeyboardButton(
                    text='📕 Правила', callback_data='uor_rules')
            ],
        ]
    )

    return markup


def agree_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Принять соглашение', callback_data='accept_agreements')
            ]
        ]
    )

    return markup


def close_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='♨️ Понятно', callback_data='to_closed')
            ]
        ]
    )

    return markup


def pay_qiwi_markup(url):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='♻️ Перейти к оплате ♻️', url=url)
            ]
        ]
    )

    return markup