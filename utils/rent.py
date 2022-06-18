from configparser import SectionProxy
import json, requests, time, aiohttp, datetime, asyncio, aiosqlite
from json.decoder import JSONDecodeError
import re
from aiogram import types
from attr import astuple

from requests.sessions import session

from data import User
from utils import config, misc, logger, Numbers, Country


class RentNumber():
    def __init__(self):
        self.errors = ['BAD_KEY', 'SQL_ERROR', 'NO_BALANCE']
        self.black_list = ['ma', 'fd', 'mg', 'md']
        self.rent_time = [4, 12, 24, 72, 168, 336]
        self.url = 'https://sms-activate.ru/stubs/handler_api.php'
        self.api = config.config("api_smsactivate")
        self.service = misc.rent
        self.country = misc.country

    def rent_name(self, code):
        return misc.service.get(code)

    def get_service(self, country):
        service = self.service.get(country)
        if service != None:
            lists = list(service.keys())
        else:
            lists = 0

        return lists

    async def get_rent_info(self, country, time):
        try:
            data = {
                'api_key': self.api,
                'action': 'getRentServicesAndCountries',
                'country': country,
                'rent_time': time
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self.url, data=data) as response:
                    if response.status == 200:
                        info = await response.text()
                        if info not in self.errors:
                            rent = json.loads(info)
                        else:
                            rent = 'ERRORS'
                    else:
                        rent = 'ERRORS'
                
        except:
            rent = 'ERORRS'

        return rent

    async def get_price(self, service, country, time):
        data = {
            'api_key': self.api,
            'action': 'getRentServicesAndCountries',
            'country': country,
            'rent_time': time
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    info = await response.text()
                    if info not in self.errors:
                        resp = json.loads(info)
                        price = resp['services'][f'{service}']
                        price = price['cost']
                    else:
                        price = 0
                else:
                    price = 0
            
        return price

    async def rent_price(self, service, country, time):
        price = await self.get_price(service, country, time)

        if price != 0:

            if time == 12:
                price = price / 100 * \
                    int(config.config("rent_percent_12h")) + price
            elif time == 24:
                price = price / 100 * \
                    int(config.config("rent_percent_24h")) + price
            elif time == 72:
                price = price / 100 * \
                    int(config.config("rent_percent_72h")) + price
            elif time == 168:
                price = price / 100 * \
                    int(config.config("rent_percent_168h")) + price
            elif time == 336:
                price = price / 100 * \
                int(config.config("rent_percent_336h")) + price
            else:
                price = price / 100 * 20 + price
        else:
            price = 0

        return round(price)

    async def rent_quant(self, country, service, time):
        data = {
            'api_key': self.api,
            'action': 'getRentServicesAndCountries',
            'country': country,
            'rent_time': time
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    info = await response.text()
                    if info not in self.errors:
                        resp = json.loads(info)
                        quant = resp['services'][service]["quant"]['current']
                    else:
                        quant = 0
                else:
                    quant = 0
            
        return quant

    async def buy_number(self, service, country, operator, time):
        try:
            data = {
                'api_key': self.api,
                'action': 'getRentNumber',
                'service': service,
                'rent_time': time,
                'operator': operator,
                'country': country,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self.url, data=data) as response:
                    if response.status == 200:
                        info = await response.text()
                        data = json.loads(info)
                        if data['status'] == 'success':
                            rent_id = data['phone']['id']
                            number = data['phone']['number']
                            date = data['phone']['endDate']
                        else:
                            if data['message'] != 'NO_NUMBERS':
                                logger.error(f'ERROR RENT: {data["message"]}')
                                rent_id = 'ERRORS'
                                number, date = 0, 0
                            else:
                                rent_id, number, date = 'NO_NUMBERS', 0, 0
                    else:
                        logger.error(f'ERROR RENT: STATUS {response.status}')
                        rent_id, number, date = 'ERRORS', 0, 0
            
        except JSONDecodeError:
            rent_id, number, date = 'ERRORS', 0, 0
        
        return rent_id, number, date


    async def status_rent(self, rent_id):
        data = {
            'api_key': self.api,
            'action': 'getRentStatus',
            'id': rent_id,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    info = await response.text()
                    if info not in self.errors:
                        data = json.loads(info)
                        if data['status'] == 'success':
                            status = data['values']
                        elif data['status'] == 'error':
                            status = 'NO_SMS'
                        else:
                            status = 'finish'
                    else:
                        status = 'ERRORS'
                else:
                    status = 'ERRORS'
                    
        return status


    async def info_rent_status(self, rent_id):
        data = {
            'api_key': self.api,
            'action': 'getRentStatus',
            'id': rent_id,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    info = await response.text()
                    data = json.loads(info)
                else:
                    logger.error(f'ERROR RENT: STATUS {response.status}')
                    data = 'ERRORS'
        
        return data


    async def update_status(self, rent_id, status):
        data = {
            'api_key': self.api,
            'action': 'setRentStatus',
            'id': rent_id,
            'status': status
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    info = await response.text()
                    data = json.loads(info)
                else:
                    logger.error(f'ERROR RENT: STATUS {response.status}')
                    data = 'ERRORS'  
        
        return data


    async def get_all_sms(self, rent_id):
        data = {
            'api_key': self.api,
            'action': 'getRentStatus',
            'id': rent_id,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                info = await response.text()
                data = json.loads(info)

            
                logs_sms = []
                if data['status'] == 'success':
                    for i in range(int(data['quantity'])):
                        sct = data['values'][str(i)]
                        logs_sms.append([sct['phoneFrom'],
                                        sct['text'],
                                        sct['service'],
                                        sct['date']])
                    
        return logs_sms

    def get_rent_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(
                text='⏱ Арендовать номер', callback_data='rent_service'),
            types.InlineKeyboardButton(
                text='⏰ Активная аренда', callback_data='my_rent_service'),
        )
        markup.add(
            types.InlineKeyboardButton(
                text='🔚 назад', callback_data='to_menu')
        )

        return markup

    def rent_time_menu(self, country, service):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(
                text=f'4 часа', callback_data=f'rent_time:{country}:{service}:4'),
            types.InlineKeyboardButton(
                text=f'12 часов', callback_data=f'rent_time:{country}:{service}:12'),
            types.InlineKeyboardButton(
                text=f'24 часа', callback_data=f'rent_time:{country}:{service}:24'),
            types.InlineKeyboardButton(
                text=f'3 дня', callback_data=f'rent_time:{country}:{service}:72')
        )

        markup.add(
            types.InlineKeyboardButton(
                text=f'7 дней', callback_data=f'rent_time:{country}:{service}:168'),
            types.InlineKeyboardButton(
                text=f'14 дней', callback_data=f'rent_time:{country}:{service}:336'),
        )
        markup.add(
            types.InlineKeyboardButton(
                text='🔚 Назад', callback_data=f'to_rent_service:{country}')
        )

        return markup

    async def buy_rent_menu(self, country, service, time):
        msg = f"""
<b>📲 Сервис:</b> {Numbers().service_name(service)} | {Country().get_country_name(country)}

<b>💳 Цена:</b> <i>{await self.rent_price(service, country, time)} RUB</i>
<b>🧿 Кол-во номеров:</b> <i>{await self.rent_quant(country, service, time)} шт</i>

<b>♻️ Нажмите купить, чтобы преобрести номер</b>
        """
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(
                text='♻️ Купить', callback_data=f'rent_buy:{country}:{service}:{time}')
        )
        markup.add(
            types.InlineKeyboardButton(
                text='🔚 Назад', callback_data=f'to_rent_time:{country}:{service}')
        )
        return msg, markup

    def rent_service_menu(self, country, page_number=1):
        service = self.get_service(country)
        markup = types.InlineKeyboardMarkup(row_width=3)
        if service != 0:

            numbers = []
            x = 1
            for i in service:
                if i not in self.black_list:
                    if i not in numbers:
                        numbers.append(i)

            rows = 15
            page = []
            pages = []
            for i in numbers:
                page.append(i)
                if len(page) == rows:
                    pages.append(page)
                    page = []

            if str(len(numbers) / rows) not in range(30):
                pages.append(page)

            x1 = 0
            x2 = 1
            x3 = 2
            for i in range(int(len(pages[page_number-1]) / 3)):
                try:
                    markup.add(
                        types.InlineKeyboardButton(text=self.rent_name(
                            pages[page_number-1][x1]), callback_data=f'buy_rent:{country}:{pages[page_number-1][x1]}'),
                        types.InlineKeyboardButton(text=self.rent_name(
                            pages[page_number-1][x2]), callback_data=f'buy_rent:{country}:{pages[page_number-1][x2]}'),
                        types.InlineKeyboardButton(text=self.rent_name(
                            pages[page_number-1][x3]), callback_data=f'buy_rent:{country}:{pages[page_number-1][x3]}'),
                    )

                    x1 += 3
                    x2 += 3
                    x3 += 3

                except:
                    pass

            previous_page_number = page_number+1 if page_number == 1 else page_number-1
            next_page_number = page_number + \
                1 if len(pages) > page_number else page_number
            if page_number == len(pages):
                previous_page_number = previous_page_number
                next_page_number = 1

            markup.add(
                types.InlineKeyboardButton(
                    text='ᐊ', callback_data=f'rent_page:{country}:{previous_page_number}'),
                types.InlineKeyboardButton(
                    text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'),
                types.InlineKeyboardButton(
                    text='ᐅ', callback_data=f'rent_page:{country}:{next_page_number}'),
                types.InlineKeyboardButton(
                    text='🔚 Назад', callback_data='to_rent'),
            )
        else:
            markup.add(
                types.InlineKeyboardButton(
                    text='Сервисов нет, попробуйте сменить страну', callback_data='oprkprekfrep')
            )
            markup.add(
                types.InlineKeyboardButton(
                    text='🔝 Меню', callback_data='to_menu'),
            )

        return markup

class RentBuyer():
    def __init__(self):
        self.errors = ['BAD_KEY', 'SQL_ERROR']
        self.sql_path = './data/database.db'

    async def buy_rents(self, user_id: int, service: str, country: int, operator: str, time: int):
        price = await RentNumber().rent_price(service, country, time)

        if float(User(user_id).balance) >= price:
            rent = await RentNumber().buy_number(service, country, operator, time)
            if rent[0] != 'ERRORS' and rent[0] != 'NO_NUMBERS':
                await User(user_id).update_balance(-price)
                rent_id, number, end_date = rent
                buy_date = datetime.datetime.now()
                await self.write_log(user_id, rent_id, number, price, buy_date, end_date, service, country, time)

                return number, end_date

            else:
                return 'NO_RENT'
        else:
            return 'NO_BALANCE'

    async def select_sms(self, bot):
        while True:
            async with aiosqlite.connect(self.sql_path) as db:
                select = await db.execute('SELECT * FROM active_rent')
                data = await select.fetchall()

            for user_id, rent_id, number, price, buy_date, end_date, service, country, time in data:

                sms = await RentNumber().status_rent(rent_id)
                if sms != 'NO_SMS' and sms != 'finish':
                    if sms != 'ERRORS':
                        for i in sms:
                            sms_info = sms[i]

                            phone = sms_info["phoneFrom"]
                            date = sms_info["date"]
                            text = sms_info["text"]

                            if not await self.check_sms_logs(rent_id, date):
                                await self.add_logs_sms(rent_id, phone, text, i, date)

                                await self.notify_user(bot, user_id, service, country, number, date, end_date, phone, text)

            await asyncio.sleep(5)


    async def notify_user(self, bot, user_id, service, country, number, sms_date, end_date, phone_from, sms_text):
        msg = f"""
<b>🧿Сервис:</b> {Numbers().service_name(service)} | {Country().get_country_name(country)}
<b>📲 Номер:</b> {number}
<b>💈 Дата сообщения:</b> {sms_date}
<b>💈 Дата окончания аренды:</b> {end_date}

<b>📫 От:</b> {phone_from}
<b>📨 Сообщение:</b> {sms_text}
        """
        await bot.send_message(chat_id=user_id, text=msg)


    async def write_log(self, user_id, rent_id, number, price, buy_date, end_date, service, country, time):
        price_service = await RentNumber().get_price(service, country, time)

        rent = [user_id, rent_id, number, price, buy_date, end_date, service, country, time]
        rent_logs = [user_id, rent_id, number, price, price_service, buy_date, end_date, service, country, time]
        async with aiosqlite.connect(self.sql_path) as db:
            sql = 'INSERT INTO active_rent VALUES (?,?,?,?,?,?,?,?,?)'
            await db.execute(sql, rent)

            sql = 'INSERT INTO logs_rent VALUES (?,?,?,?,?,?,?,?,?,?)'
            await db.execute(sql, rent_logs)
            await db.commit()

    async def check_sms_logs(self, rent_id, sms_date):
        async with aiosqlite.connect(self.sql_path) as db:
            sql = "SELECT * FROM sms_rent WHERE rent_id = ? AND sms_date = ?"
            select = await db.execute(sql, (rent_id, sms_date))
            data = await select.fetchall()
            await select.close()
            if data:
                return True
            else:
                return False


    async def add_logs_sms(self, rent_id, phone, sms_text, sms_id, sms_date):
        async with aiosqlite.connect(self.sql_path) as db:
            sql = "INSERT INTO sms_rent VALUES (?, ?, ?, ?, ?)"
            await db.execute(sql, (rent_id, phone, sms_text, sms_id, sms_date))
            await db.commit()

    async def get_active_rent(self, user_id):
        async with aiosqlite.connect(self.sql_path) as db:
            select = await db.execute(f'SELECT * FROM active_rent WHERE user_id = "{user_id}"')
            numbers = await select.fetchall()
            await select.close()

            base = []

            for i in numbers:
                if datetime.datetime.fromisoformat(i[5]) < datetime.datetime.now():
                    await db.execute(f'DELETE FROM active_rent WHERE rent_id = "{i[1]}"')
                    await db.commit()
                else:
                    base.append(i)

        return base

    async def get_menu_my_rent(self, user_id):
        numbers = await self.get_active_rent(user_id)

        markup = types.InlineKeyboardMarkup(row_width=2)

        for i in numbers:
            markup.add(types.InlineKeyboardButton(text=f'{i[2]} | {Numbers().service_name(i[6])} | {Country().get_country_name(i[7])}', 
                                        callback_data=f'my_rent:{i[1]}'))

        markup.add(
            types.InlineKeyboardButton(text='🔙', callback_data='to_rent'))

        return markup

    async def my_rent_info(self, rent_id):
        await self.get_info_rent(rent_id)

        all_msg = await RentNumber().get_all_sms(rent_id)
        msg = ''
        number = 0

        if len(all_msg) == 0:
            txt = """
<i>Ожидаем сообщение...</i>


<i>⚠️ Вы можете отменить аренду номера в течении 15 минут, при условии того, что на него не было получено SMS.</i>
            """
        else:
            message = 0
            for i in all_msg:
                message += 1
                number += 1
                msg += f'{number}. <b>Отправитель:</b> <i>{i[0]}</i>\n <b>Дата:</b> <i>{i[3]}</i>\n <b>Сообщение:</b> {i[1]}\n\n'

                if message >= 3:
                    break

            txt = f"""
<b>Данные о номере.</b>

<b>📞 Номер телефона:</b> <code>{self.number}</code>
<b>🛠 Сервис:</b> <i>{Numbers().service_name(self.service)}</i>
<b>🚩 Страна:</b> <i>{Country().get_country_name(self.country)}</i>
<b>⏰ Дата окончания:</b> <i>{self.end_date}</i>

<b>📝 История SMS:</b> 
{msg}
            """
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(text='❌ Отменить аренду', callback_data=f'rent_cancel:{rent_id}'), 
            types.InlineKeyboardButton(text='🔙 назад', callback_data='to_menu'), 
        )

        return txt, markup



    async def get_info_rent(self, rent_id):
        async with aiosqlite.connect(self.sql_path) as db:
            select = await db.execute(f'SELECT * FROM logs_rent WHERE rent_id = "{rent_id}"')
            info = await select.fetchone()
            await select.close()

        self.user_id = info[0]
        self.rent_id = info[1]
        self.number = info[2]
        self.price = info[3]
        self.price_service = info[4]
        self.buy_date = info[5]
        self.end_date = info[6]
        self.service = info[7]
        self.country = info[8]
        self.time = info[9]

        return info

    async def cancel_rent(self, rent_id):

        await self.get_info_rent(rent_id)
        rent = await RentNumber().info_rent_status(rent_id)

        bad_text = f'<b>❌ Аренда номера +{self.number} не может быть отменена!\n\n ✋🏼Вероятнее всего вы нарушили условия.</b>'
        if rent != 'ERRORS':
            if rent['status'] != 'success':
                async with aiosqlite.connect(self.sql_path) as db:
                    sql = 'SELECT buy_date FROM active_rent WHERE rent_id = ?'

                    select = await db.execute(sql, (rent_id, ))
                    rent_info = await select.fetchone()
                    await select.close()

                    date = datetime.datetime.strptime(rent_info[0], '%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(minutes=15)

                    if date > datetime.datetime.now():
                        await db.execute(f'DELETE FROM active_rent WHERE rent_id = "{rent_id}"')
                        await db.commit()


                        status = await RentNumber().update_status(rent_id, 2)
                        if status != 'ERRORS':
                            if status['status'] == 'success':
                                await User(self.user_id).update_balance(self.price)
                                await db.execute(f'DELETE FROM logs_rent WHERE rent_id = "{rent_id}"')
                                await db.commit()

                                text = f'<b>✅ Аренда номера +{self.number} отменена.\n\n🏵На баланс зачислено + {self.price} рублей.</b>'
                            else:
                                text = bad_text
                        else:
                            text = bad_text
                    else:
                        text = bad_text
            else:
                text = bad_text
        else:
            text = bad_text
        
        return text

    async def admin_rent_menu(self):
        async with aiosqlite.connect(self.sql_path) as db:
            select = await db.execute(f'SELECT * FROM active_rent')
            numbers = await select.fetchall()
            await select.close()

            rent = list(numbers)

            if len(rent) > 0:
                base = []

                for i in numbers:
                    if datetime.datetime.fromisoformat(i[5]) < datetime.datetime.now():
                        await db.execute(f'DELETE FROM active_rent WHERE rent_id = "{i[1]}"')
                        await db.commit()
                    else:
                        base.append(i)

                markup = types.InlineKeyboardMarkup(row_width=1)

                for i in base:
                    markup.add(
                        types.InlineKeyboardButton(text=f'{User(i[0]).username} | {i[2]}', callback_data=f'adm_rent_info:{i[1]}')
                    )

                return markup
            else:
                return False

    async def admin_rent_info(self, rent_id):
        async with aiosqlite.connect(self.sql_path) as db:
            select = await db.execute(f'SELECT * FROM active_rent WHERE rent_id = "{rent_id}"')
            rent = await select.fetchone()
            await select.close()

        msg = f"""
<b>🧿 Cервис:</b> {Numbers().service_name(rent[6])} | {Country().get_country_name(rent[7])}
<b>🛡 Время:</b> {rent[8]} ч
<b>📞 Номер:</b> +{rent[2]}

<b>Дата покупки:</b> {rent[4]}
<b>Дата окончания:</b> {rent[5]}

<b>🧬 Покупатель:</b> @{User(rent[0]).username} | {rent[0]}
"""
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(text='Удалить', callback_data=f'adm_del_rent:{rent_id}'),
            types.InlineKeyboardButton(text='Закрыть', callback_data=f'to_closed')
        )

        return msg, markup

    async def admin_delete_rent(self, rent_id):
        await self.get_info_rent(rent_id)
        rent = await RentNumber().info_rent_status(rent_id)

        bad_text = f'<b>❌ Аренда номера +{self.number} не может быть отменена! Прошло больше 20 мин или же пришли коды</b>'
        if rent != 'ERRORS':
            if rent['status'] != 'success':
                async with aiosqlite.connect(self.sql_path) as db:

                    sql = 'SELECT buy_date FROM active_rent WHERE rent_id = ?'
                    select = await db.execute(sql, (rent_id, ))
                    rent_info = await select.fetchone()
                    await select.close()


                    date = datetime.datetime.strptime(rent_info[0], '%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(minutes=19)

                    if date > datetime.datetime.now():
                        await db.execute(f'DELETE FROM active_rent WHERE rent_id = "{rent_id}"')
                        await db.commit()

                        status = await RentNumber().update_status(rent_id, 2)
                        if status != 'ERRORS':
                            if status['status'] == 'success':
                                await User(self.user_id).update_balance(self.price)
                                await db.execute(f'DELETE FROM logs_rent WHERE rent_id = "{rent_id}"')
                                await db.commit()

                                text = f'<b>✅ Аренда номера +{self.number} отменена.\n\n🏵 @{User(self.user_id).username} на баланс зачислено + {self.price} рублей.</b>'
                            else:
                                text = bad_text
                        else:
                            text = bad_text
                    else:
                        text = bad_text
            else:
                text = bad_text
        else:
            text = bad_text
        
        return text

