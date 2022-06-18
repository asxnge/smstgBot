from aiogram import types
import sqlite3, datetime, time

from data import functions as func


def get_users():
    conn, cursor = func.connect()

    users = cursor.execute(f'SELECT * FROM users').fetchall()

    return users

def admin_stats():
    conn, cursor = func.connect()

    cursor.execute(f'SELECT * FROM users')
    row = cursor.fetchall()

    day = datetime.timedelta(days=1)
    hour = datetime.timedelta(hours=1)
    date = datetime.datetime.now()

    amount_user_all = 0
    amount_user_day = 0
    amount_user_hour = 0

    for i in row:
        amount_user_all += 1

        if date - datetime.datetime.fromisoformat(i[6]) <= day:
            amount_user_day += 1
        if date - datetime.datetime.fromisoformat(i[6]) <= hour:
            amount_user_hour += 1

    cursor.execute(f'SELECT * FROM deposit_logs')
    pay = cursor.fetchall()

    qiwi = 0
    all_qiwi = 0
    banker = 0
    all_banker = 0
    chatex = 0
    all_chatex = 0

    for i in pay:
        if i[2] == 'qiwi':
            if date - datetime.datetime.fromisoformat(i[4]) <= day:
                qiwi += float(i[3])

            all_qiwi += float(i[3])

        elif i[2] == 'banker':
            if date - datetime.datetime.fromisoformat(i[4]) <= day:
                banker += float(i[3])

            all_banker += float(i[3])
        elif i[2] == 'chatex':
            if date - datetime.datetime.fromisoformat(i[4]) <= day:
                chatex += float(i[3])

            all_chatex += float(i[3])


    msg = f"""
<b>💈 Информация о пользователях:</b>

❕ За все время: <b>{amount_user_all}</b>
❕ За день: <b>{amount_user_day}</b>
❕ За час: <b>{amount_user_hour}</b>

<b>💈 Пополнений за 24 часа</b>
❕ QIWI: <b>{qiwi} ₽</b>
❕ Banker: <b>{banker} ₽</b>
❕ Chatex: <b>{chatex} ₽</b>

<b>💈 Ниже приведены данные за все время</b>
💳 Пополнения QIWI: <b>{all_qiwi} ₽</b>
💳 Пополнения BANKER: <b>{all_banker} ₽</b>
💳 Пополнения Chatex: <b>{all_chatex} ₽</b>
{func.System().info_msg()}
"""

    return msg

def admin_marg():
    conn, cursor = func.connect()

    cursor.execute('SELECT * FROM service_logs')
    row = cursor.fetchall()

    spending_all = 0
    spending_90d = 0
    spending_month = 0
    spending_7d = 0
    spending_day = 0
    spending_hour = 0

    profit_all = 0
    profit_90d = 0
    profit_month = 0
    profit_7d = 0
    profit_day = 0
    profit_hour = 0

    good_act = 0
    good_act_90d = 0
    good_act_month = 0
    good_act_7d = 0
    good_act_day = 0

    for i in row:
        if i[7] == 'good' or i[7] == 'more_good':
            spending_all += float(i[5])
            profit_all += float(i[5]) - float(i[6])
            good_act += 1

            if time.time() - float(i[8]) <= 7776000:
                spending_90d += float(i[5])
                profit_90d += float(i[5]) - float(i[6])
                good_act_90d += 1

            if time.time() - float(i[8]) <= 2592000:
                spending_month += float(i[5])
                profit_month += float(i[5]) - float(i[6])
                good_act_month += 1

            if time.time() - float(i[8]) <= 604800:
                spending_7d += float(i[5])
                profit_7d += float(i[5]) - float(i[6])
                good_act_7d += 1

            if time.time() - float(i[8]) <= 86400:
                spending_day += float(i[5])
                profit_day += float(i[5]) - float(i[6])
                good_act_day += 1

            if time.time() - float(i[8])  <= 3600:
                spending_hour += float(i[5])
                profit_hour += float(i[5]) - float(i[6])

    cursor.execute('SELECT * FROM logs_rent')
    row = cursor.fetchall()

    day = datetime.timedelta(days=1)
    day7 = datetime.timedelta(days=7)
    month = datetime.timedelta(weeks=1)
    day90 = datetime.timedelta(weeks=3)
    hour = datetime.timedelta(hours=1)
    date = datetime.datetime.now()

    good_rent = 0
    good_rent_90d = 0
    good_rent_month = 0
    good_rent_7d = 0
    good_rent_day = 0

    for i in row:
        spending_all += float(i[3])
        profit_all += float(i[3]) - float(i[4])
        good_rent += 1

        if date - datetime.datetime.fromisoformat(i[5]) <= day90:
            spending_90d += float(i[3])
            profit_90d += float(i[3]) - float(i[4])
            good_rent_90d += 1
        
        if date - datetime.datetime.fromisoformat(i[5]) <= month:
            spending_month += float(i[3])
            profit_month += float(i[3]) - float(i[4])
            good_rent_month += 1

        if date - datetime.datetime.fromisoformat(i[5]) <= day7:
            spending_7d += float(i[3])
            profit_7d += float(i[3]) - float(i[4])
            good_rent_7d += 1

        if date - datetime.datetime.fromisoformat(i[5]) <= day:
            spending_day += float(i[3])
            profit_day += float(i[3]) - float(i[4])
            good_rent_day += 1

        if date - datetime.datetime.fromisoformat(i[5]) <= hour:
            spending_hour += float(i[3])
            profit_hour += float(i[3]) - float(i[4])

    msg = f"""
🚸Пользователи потратили за все время: {round(spending_all)} ₽
〽️ Маржа за все время: {round(profit_all)} ₽

🚸 Пользователи потратили за 90 дней: {round(spending_90d)} ₽
〽️ Маржа за 90 дней: {round(profit_90d)} ₽

🚸 Пользователи потратили за 30 дней: {round(spending_month)} ₽
〽️ Маржа за 30 дней: {round(profit_month)} ₽

🚸 Пользователи потратили за 7 дней: {spending_7d} ₽
〽️ Маржа за 7 дней: {round(profit_7d)} ₽

🚸 Пользователи потратили за сутки: {spending_day} ₽
〽️ Маржа за сутки: {round(profit_day)} ₽

🚸 Пользователи потратили за час: {spending_hour} ₽
〽️ Маржа за час: {round(profit_hour)} ₽

<b>💈 Активации:</b>
🌀 Успешных активаций за все время: <b>{good_act} шт</b>
🌀 Успешных активаций за 90 дней: <b>{good_act_90d} шт</b>
🌀 Успешных активаций за 30 дней: <b>{good_act_month} шт</b>
🌀 Успешных активаций за 7 дней: <b>{good_act_7d} шт</b>
🌀 Успешных активаций за сутки: <b>{good_act_day} шт</b>

<b>💈 Данные по аренде:</b>
🌀 Аренд за все время: <b>{good_rent} шт</b>
🌀 Аренд за 90 дней: <b>{good_rent_90d} шт</b>
🌀 Аренд за 30 дней: <b>{good_rent_month} шт</b>
🌀 Аренд за 7 дней: <b>{good_rent_7d} шт</b>
🌀 Аренд за сутки: <b>{good_rent_day} шт</b>
    """

    return msg

def down_sending(types, text, photo, date):
    conn, cursor = func.connect()

    data = [types, text, photo, date]
    sql = 'INSERT INTO sending VALUES (?,?,?,?)'

    cursor.execute(sql, data)
    conn.commit()

def sending_check():
    conn, cursor = func.connect()
    
    cursor.execute(f'SELECT * FROM sending')
    row = cursor.fetchall()

    for i in row:
        if datetime.datetime.fromisoformat(i[3]) <= datetime.datetime.now():
            cursor.execute(f'DELETE FROM sending WHERE photo = "{i[2]}"')
            conn.commit()

            return i

    return False

def down_sending_markup():
    conn, cursor = func.connect()
    cursor.execute(f'SELECT * FROM sending')
    info = cursor.fetchall()
    if len(info) > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        x1 = 0
        x2 = 1
        try:
            for i in range(len(info)):
                markup.add(
                    types.InlineKeyboardButton(text=f'💈 {info[x1][3]} 📝{info[x1][1]}', callback_data=f'info_sending:{info[x1][2]}'),
                    types.InlineKeyboardButton(text=f'💈 {info[x2][3]} 📝{info[x2][1]}', callback_data=f'info_sending:{info[x2][2]}')
                )

                x1 += 2
                x2 += 2
        except:
            try:
                markup.add(
                    types.InlineKeyboardButton(text=f'💈 {info[x1][3]} 📝{info[x1][1]}', callback_data=f'info_sending:{info[x1][2]}')
                )
            except:
                return markup

        return markup

    else:
        return False

def down_sending_info(code):
    conn, cursor = func.connect()
    
    cursor.execute(f'SELECT * FROM sending WHERE photo = "{code}"')
    info = cursor.fetchone()

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add( 
        types.InlineKeyboardButton(text=f'Удалить', callback_data=f'del_sending:{code}'),
        types.InlineKeyboardButton(text=f'Выйти', callback_data=f'to_closed'),
    )

    msg = f"""
<b>🖲 Тип рассылки:</b> {info[0]}
<b>🗒 Текст:</b>
{info[1]}
<b>📆 Дата:</b> {info[3]}
    """

    return msg, markup

def del_sending(code):
    conn, cursor = func.connect()
    cursor.execute(f'DELETE FROM sending WHERE photo = "{code}"')
    conn.commit()


def add_button(name, info, photo):
    conn, cursor = func.connect()
    
    cursor.execute(f'INSERT INTO buttons VALUES ("{name}", "{info}", "{photo}")')
    conn.commit()

def btn_menu_list():
    conn, cursor = func.connect()

    cursor.execute(f'SELECT * FROM buttons')
    base = cursor.fetchall()
    btn_list = []
    for i in base:
        btn_list.append(i[0])

    return btn_list

def info_buttons(name):
    conn, cursor = func.connect()

    cursor.execute(f'SELECT * FROM buttons WHERE name = "{name}"')
    info = cursor.fetchone()

    return info

def buttons_markup():
    conn, cursor = func.connect()
    cursor.execute(f'SELECT * FROM buttons')
    info = cursor.fetchall()
    if len(info) > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        x1 = 0
        x2 = 1
        try:
            for i in range(len(info)):
                markup.add(
                    types.InlineKeyboardButton(text=f'🌀 {info[x1][0]} ', callback_data=f'info_btn:{info[x1][2]}'),
                    types.InlineKeyboardButton(text=f'🌀 {info[x2][0]} ', callback_data=f'info_btn:{info[x2][2]}')
                )

                x1 += 2
                x2 += 2
        except:
            try:
                markup.add(
                    types.InlineKeyboardButton(text=f'🌀 {info[x1][0]}', callback_data=f'info_btn:{info[x1][2]}')
                )
            except:
                return markup

        return markup

    else:
        return False

def btn_info(code):
    conn, cursor = func.connect()
    
    cursor.execute(f'SELECT * FROM buttons WHERE photo = "{code}"')
    info = cursor.fetchone()

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add( 
        types.InlineKeyboardButton(text=f'Удалить', callback_data=f'del_btn:{code}'),
        types.InlineKeyboardButton(text=f'Выйти', callback_data=f'to_closed'),
    )

    msg = f"""
<b>🌀 Название кнопки:</b> {info[0]}
<b>🗒 Описание:</b>
{info[1]}
    """

    return msg, markup

def delete_button(code):
    conn, cursor = func.connect()
    
    cursor.execute(f'DELETE FROM buttons WHERE photo = "{code}"')
    conn.commit()

def payments_user_markup(user_id):
    conn, cursor = func.connect()
    cursor.execute(f'SELECT * FROM deposit_logs WHERE user_id = "{user_id}"')
    info = cursor.fetchall()
    if len(info) > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        x1 = 0
        x2 = 1
        try:
            for i in range(len(info)):
                markup.add(
                    types.InlineKeyboardButton(
                            text=f'🌀 {info[x1][2]} | {info[x1][3]} RUB', callback_data=f'info_pay:{info[x1][0]}'),
                    types.InlineKeyboardButton(
                            text=f'🌀 {info[x2][2]} | {info[x2][3]} RUB ', callback_data=f'info_pay:{info[x2][0]}')
                )

                x1 += 2
                x2 += 2
        except:
            try:
                markup.add(
                    types.InlineKeyboardButton(
                            text=f'🌀 {info[x1][2]} | {info[x1][3]} RUB', callback_data=f'info_pay:{info[x1][0]}')
                )
            except:
                return markup

        return markup

    else:
        return False