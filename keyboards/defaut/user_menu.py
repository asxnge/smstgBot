from aiogram import types
from data import functions as func

store_buttons = [
    '📩 Номера',
    '🧑🏻‍💻 Кабинет',
    '📜 Информация',
]


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(store_buttons[0], store_buttons[1])
    markup.add(store_buttons[2])

    conn, cursor = func.connect()

    base = cursor.execute(f'SELECT * FROM buttons').fetchall()
    x1 = 0
    x2 = 1
    try:
        for i in range(len(base)):
            markup.add(base[x1][0], base[x2][0])
            x1 += 2
            x2 += 2
    except:
        try:
            markup.add(base[x1][0])
        except:
            return markup

    return markup
