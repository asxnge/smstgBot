from aiogram import types

admin_button = [
    '📊 Cтатистика',
    '🔗 Рассылка',
    '⚙️ Настройки',
    '🔍 Поиск юзера',
    '🔚 Назад'
]

admin_settings_btn = [
    'Qiwi',
    'Кнопки',
    'Аренда',
    'API Сервисов',
    'Наценка',
    '🔚 Назад',

]

admin_sending_btn = [
    '✅ Начать',
    '🔧 Отложить',
    '❌ Отменить'
]


def admin_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        admin_button[0],
        admin_button[1],
        admin_button[2],
        admin_button[3],
    )
    markup.add(
        admin_button[4]
    )
    return markup


def admin_settings():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(admin_settings_btn[0], admin_settings_btn[1],
            admin_settings_btn[2], admin_settings_btn[3], admin_settings_btn[4]
    )
    markup.add(admin_settings_btn[5],
    )
    return markup


def admin_sending():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        admin_sending_btn[0],
        admin_sending_btn[1],
        admin_sending_btn[2],
    )

    return markup
