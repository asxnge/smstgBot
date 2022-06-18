from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp, aiosqlite, json, time, asyncio
from aiogram import types

from data import User
from utils import config, logger, Numbers, Country

buy_text = """
<b>🧿 Cервис:</b> {service}
<b>🌏 Cтрана:</b> {country}
<b>💈 Номер:</b> <code>{number}</code>
<i>⏱Ожидайте код... 
🕑В случае если код не придет в течении 5 минут, вам вернутся деньги на баланс.</i>
"""

more_code_text = """
<b>🧿 Cервис:</b> {service} | {country}

<b>💈 Номер:</b> <code>{number}</code>
<b>📮 Повторный код:</b> <code>{code}</code>
"""

good_code_text = """
<b>🧿 Cервис:</b> {service} | {country}

<b>💈 Номер:</b> <code>{number}</code>
<b>📮 Cмс код:</b> <code>{code}</code>
"""

class Activate():
    def __init__(self):
        self.errors = ['BAD_ACTION', 'BAD_KEY', 'ERROR_SQL',
                       'NO_BALANCE', 'WRONG_SERVICE', 'NO_ACTIVATION']
        self.url = 'https://sms-activate.ru/stubs/handler_api.php'
        self.api = config.config("api_smsactivate")

    async def get_price(self, country, service):
        try:
            data = {
                'api_key': self.api,
                'action': 'getPrices',
                'service': service,
                'country': country,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self.url, data=data) as response:
                    if response.status == 200:
                        info = await response.text()
                        info = json.loads(info).get(f'{country}')
                        price = info[f'{service}']['cost']
                    else:
                        logger.error(f'ERROR SMS ACTIVATE: STATUS {response.status}')
                        price = 0
        except:
            price = 0

        return price

    async def get_balance(self):
        data = {
            "api_key": self.api,
            "action": "getBalance",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    info = await response.text()
                    if info not in self.errors:
                        balance = str(info).split(":")[1]
                    else:
                        logger.error(f'ERRORS: {info}')
                        balance = 0
                else:
                    logger.error(f'ERROR SMS ACTIVATE: STATUS {response.status}')
                    balance = 0
        
        return balance

    async def get_numbers_quantity(self, country: int, service: str, operator: str):
        data = {
            'api_key': self.api,
            'action': 'getNumbersStatus',
            'country': country,
            'operator': operator
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    info = await response.text()
                    if info not in self.errors:
                        data = json.loads(info)
                        count = data.get(f'{service}_0')
                    else:
                        logger.error(f'ERRORS: {info}')
                        count = 0
                else:
                    logger.error(f'ERROR SMS ACTIVATE: STATUS {response.status}')
                    count = 0
            
        
        return count

    async def buy_service(self, country: int, service: str, operator: str):
        data = {
            'api_key': self.api,
            'action': 'getNumber',
            'service': service,
            'operator': operator,
            'country': country,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200 or response.status == 502:
                    info = await response.text()
                    if info not in self.errors:
                        if 'NO_NUMBERS' not in info:
                            service = info
                        else:
                            service = f'ERRORS:{info}'
                    else:
                        service = f'ERRORS:{info}'
                else:
                    logger.error(f'ERROR SMS ACTIVATE: STATUS: {response.status}')
                    service = f'ERRORS:NO_NUMBERS'


        return service

    async def set_status(self, operation_id: str, status: int):
        data = {
            'api_key': self.api,
            'action': 'setStatus',
            'status': status,
            'id': operation_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                info_status = await response.text()


        return info_status 

    async def get_status(self, operation_id: str):
        data = {
            'api_key': self.api,
            'action': 'getStatus',
            'id': operation_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    info = await response.text()
                    if info not in self.errors:
                        status = info
                    else:
                        logger.error(f'ERROR: {info}')
                        status = 'ERRORS'
                else:
                    status = 'ERRORS'
                    
        return status

    async def get_fullsms(self, operation_id):
        data = {
            'api_key': self.api,
            'action': 'getFullSms',
            'id': operation_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    status = await response.text()
                    if status not in self.errors:
                        if 'FULL_SMS:' in status:
                            full_sms = status.split(":")[1]
                        else:
                            full_sms = 'WAIT_OR_CANCEL'
                    else:
                        full_sms = 'ERRORS'
                else:
                    full_sms = 'ERRORS'
                    logger.error(f'ERROR SMS ACTIVATE: STATUS {response.status}')
            
        return full_sms

class HUB():
    def __init__(self):
        self.errors = ['BAD_ACTION', 'BAD_KEY', 'ERROR_SQL',
                       'NO_BALANCE', 'WRONG_SERVICE', 'NO_ACTIVATION']
        self.url = 'https://smshub.org/stubs/handler_api.php'
        self.api = config.config("api_smshub")

    async def get_price(self, country: int, service: str):
        try:
            data = {
                'api_key': self.api,
                'action': 'getPrices',
                'service': service,
                'country': country
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self.url, data=data) as response:
                    if response.status == 200:
                        info = await response.text()
                        if info not in self.errors:
                            resp = json.loads(info).get(f'{country}')
                            if resp != {}:
                                price = list(resp[f'{service}'].keys())
                                price = price[0]
                            else:
                                price = 0
                        else:
                            price = 0
                    else:
                        logger.error(f'ERROR SMS HUB: STATUS {response.status}')
                        price = 0
        except:
            price = 0

        return price


    async def get_balance(self):
        data = {
            "api_key": self.api,
            "action": "getBalance",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    balance = await response.text()
                    if balance not in self.errors:
                        balance = balance.split(":")[1]
                    else:
                        balance = 0
                else:
                    logger.error(f'ERROR SMS HUB: STATUS {response.status}')
                    balance = 0
        
        return balance

    async def get_numbers_quantity(self, country, service, operator):
        try:
            data = {
                'api_key': self.api,
                'action': 'getNumbersStatus',
                'country': country,
                'operator': operator
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self.url, data=data) as response:
                    if response.status == 200:
                        info = await response.text()
                        if info not in self.errors:
                            resp = json.loads(info)
                            count = resp.get(f'{service}_0')
                        else:
                            count = 0
                    else:
                        logger.error(f'ERROR SMSHUB: STATUS {response.status}')
                        count = 0
        except:
            count = 0

        return count

    async def buy_service(self, country: int, service: str, operator: str):
        data = {
            'api_key': self.api,
            'action': 'getNumber',
            'service': service,
            'operator': operator,
            'country': country,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200 or response.status == 502:
                    info = await response.text()
                    if info not in self.errors:
                        if 'NO_NUMBERS' not in info:
                            service = info
                        else:
                            service = f'ERRORS:{info}'
                    else:
                        service = f'ERRORS:{info}'
                else:
                    logger.error(f'ERROR SMSHUB: STATUS {response.status}')
                    service = f'ERRORS:NO_NUMBERS'
        
        return service
        


    async def set_status(self, operation_id: str, status: int):
        data = {
            'api_key': self.api,
            'action': 'setStatus',
            'status': status,
            'id': operation_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    info_status = await response.text()
                else:
                    info_status = 'ERRORS'
        
        return info_status


    async def get_status(self, operation_id: str):
        data = {
            'api_key': self.api,
            'action': 'getStatus',
            'id': operation_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, data=data) as response:
                if response.status == 200:
                    info = await response.text()
                    if info not in self.errors:
                        status = info
                    else:
                        status = 'ERRORS'
                else:
                    logger.error(f'ERROR SMSHUB: STATUS {response.status}')
                    status = 'ERRORS'
                    
        return status

class SMSService():
    def __init__(self, obj=None):
        self.sql_path = './data/database.db'
        if obj != None:
            self.wait = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self.wait)
        except StopIteration:
            raise StopAsyncIteration
        return value

    async def write_sms_list(self, user_id, operation_id, number, service, country, price, provider):
        async with aiosqlite.connect(self.sql_path) as db:
            sms = [user_id, operation_id, number, service, country, 'first', time.time(), price, provider]
            await db.execute('INSERT INTO wait_sms VALUES (?,?,?,?,?,?,?,?,?)', sms)
            await db.commit()

    async def del_wait_sms(self, operation_id: str):
        async with aiosqlite.connect(self.sql_path) as db:

            await db.execute(f'DELETE FROM wait_sms WHERE operation_id = "{operation_id}"')
            await db.commit()

    async def write_logs(self, user_id: int, operation_id: str, service: str, country: int, number: str, price: float, status: str):
        price_service = await Activate().get_price(country, service)
        async with aiosqlite.connect(self.sql_path) as db:
            sms = [user_id, operation_id, service, country, number, price, price_service, status, time.time()]

            await db.execute('INSERT INTO service_logs VALUES (?,?,?,?,?,?,?,?,?)', sms)
            await db.commit()

    async def get_info_sms(self, operation_id: int):
        async with aiosqlite.connect(self.sql_path) as db:

            select = await db.execute(f'SELECT * FROM wait_sms WHERE operation_id = "{operation_id}"')
            service = await select.fetchone()
            await select.close()

        return service

    async def update_wait_status(self, operation_id: str, status: str):
        async with aiosqlite.connect(self.sql_path) as db:

            await db.execute(f'UPDATE wait_sms SET status = "{status}" WHERE operation_id = "{operation_id}"')
            await db.commit()

    async def add_notify(self, user_id, service, country, operator):
        async with aiosqlite.connect(self.sql_path) as db:
            sql = 'INSERT INTO notify_numbers VALUES (?,?,?,?)'
            await db.execute(sql, (user_id, service, country, operator))
            await db.commit()

    async def buy_service(self, bot, user_id, service, country, operator):
        price = await Numbers().get_service_price(country, service)
        text_error = 'Извините, у нас небольшие неполадки'
        text_no_number = 'Кажется закончились номера, попробуйте позже'

        if float(User(user_id).balance) >= float(price):
            price_hub = await HUB().get_price(country, service)
            price_activate = await Activate().get_price(country, service)

            if float(price_activate) >= float(price_hub) and price_hub != 0:

                code = await self.buy_hub(bot, user_id, service, country, operator, price)
                if code != 'ACCESS':
                    code = await self.buy_activate(bot, user_id, service, country, operator, price)
                    if code != 'ACCESS':
                        if code == 'NO_NUMBERS':
                            markup = self.notify_markup(service, country, operator)
                            await bot.send_message(chat_id=user_id, text=text_no_number, reply_markup=markup)
                        elif code == 'ERRORS':
                           await bot.send_message(chat_id=user_id, text=text_error)
            else:
                code = await self.buy_activate(bot, user_id, service, country, operator, price)
                if code != 'ACCESS':
                    code = await self.buy_hub(bot, user_id, service, country, operator, price)
                    if code != 'ACCESS':
                        if code == 'NO_NUMBERS':
                            markup = self.notify_markup(service, country, operator)
                            await bot.send_message(chat_id=user_id, text=text_no_number, reply_markup=markup)
                        elif code == 'ERRORS':
                            await bot.send_message(chat_id=user_id, text=text_error)
        else:
            await bot.send_message(chat_id=user_id, text='Пополните баланс!')

    async def buy_hub(self, bot, user_id, service, country, operator, price):
        services = await HUB().buy_service(country, service, operator)
        if services.split(":")[0] == 'ACCESS_NUMBER':
            operation_id, number = services.split(":")[1], services.split(":")[2]
            text = buy_text.format(service=Numbers().service_name(service), 
                            country=Country().get_country_name(country), number=number)

            await HUB().set_status(operation_id, 1)
            await User(user_id).update_balance(-float(price))

            await bot.send_message(chat_id=user_id, text=text)

            await self.write_sms_list(user_id, operation_id, number, service, country, price, 'SMSHub')
            code = 'ACCESS'
        else:
            if services.split(":")[1] == 'NO_NUMBERS':
                code = 'NO_NUMBERS'
            else:
                code = 'ERRORS'

        return code


    async def buy_activate(self, bot, user_id, service, country, operator, price):

        services = await Activate().buy_service(country, service, operator)
        if services.split(":")[0] == 'ACCESS_NUMBER':
            operation_id, number = services.split(":")[1], services.split(":")[2]
            text = buy_text.format(service=Numbers().service_name(service), 
                            country=Country().get_country_name(country), number=number)

            await Activate().set_status(operation_id, 1)
            await User(user_id).update_balance(-float(price))

            await bot.send_message(chat_id=user_id, text=text)

            await self.write_sms_list(user_id, operation_id, number, service, country, price, 'SMSActivate')
            code = 'ACCESS'
        else:
            if services.split(":")[1] == 'NO_NUMBERS':
                code = 'NO_NUMBERS'
            else:
                code = 'ERRORS'
        
        return code
    
    def notify_markup(self, service, country, operator):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='🛎 Оповестить об пополнении', callback_data=f'notify_me:{service}:{country}:{operator}')
                ]
            ]
        )

        return markup

    async def cancel_number(self, user_id: int, operation_id: str, price: float, provider: str):
        if provider == 'SMSHub':
            status = await HUB().get_status(operation_id)
            if status != 'STATUS_CANCEL' and 'STATUS_OK:' not in status:
                await User(user_id).update_balance(+float(price))
                await HUB().set_status(operation_id, 8)

                text = f'Номер отменен, и на ваш баланс вернулось + {price} RUB'
            else:
                text = 'Номер уже использован'
        else:
            status = await Activate().get_status(operation_id)
            if status != 'STATUS_CANCEL' and 'STATUS_OK:' not in status:
                await User(user_id).update_balance(+float(price))
                await Activate().set_status(operation_id, 8)

                text = f'Номер отменен, и на ваш баланс вернулось + {price} RUB'
            else:
                text = 'Номер уже использован'
        
        return text

    async def sms_code(self, operation_id, provider):
        if provider == 'SMSHub':
            status = await HUB().get_status(operation_id)
            if 'STATUS_OK:' in status:
                code = status[10:]
            else:
                code = 'ERRORS'
        else:
            status = await Activate().get_status(operation_id)
            if 'STATUS_OK:' in status:
                full_sms = await Activate().get_fullsms(operation_id)
                if full_sms != 'ERRORS' and full_sms != 'WAIT_OR_CANCEL':
                    codes = full_sms
                    code = ''
                    sms = 0
                    for i in codes:
                        sms += 1
                        if not sms == 1:
                            code =  f'{code}{i}'

                    code = f'SMS: {code} КОД: {status[10:]}'

                else:
                    code = status[10:]
            else:
                code = 'ERRORS'
        
        return code


    
    def get_wait_menu(self, service: str, number: str, operation_id: str, price: float, provider: str):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(
                text='Завершить', callback_data=f'end_number:{operation_id}:{provider}'),
            types.InlineKeyboardButton(
                text='Еще смс', callback_data=f'still_number:{service}:{number}:{operation_id}:{price}:{provider}')
        )

        return markup

    def menu_end(self, operation_id, provider):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(text='Завершить', callback_data=f'end_number:{operation_id}:{provider}'),
        )
        return markup

    async def end_service(self, operation_id: str, provider: str):
        if provider == 'SMSHub':
            await HUB().set_status(operation_id, 6)
            await self.del_wait_sms(operation_id)
        else:
            await Activate().set_status(operation_id, 6)
            await self.del_wait_sms(operation_id)

    async def set_status(self, operation_id: str, provider: str, status: int):
        if provider == 'SMSHub':
            await HUB().set_status(operation_id, status)
        else:
            await Activate().set_status(operation_id, status)

    async def check_count_numbers(self, bot):
        while True:
            await asyncio.sleep(5)
            async with aiosqlite.connect(self.sql_path) as db:
                select = await db.execute('SELECT* FROM notify_numbers')
                lists = await select.fetchall()
                await select.close()


            for i in lists:
                await asyncio.sleep(3)
                count_activate = await Activate().get_numbers_quantity(i[2], i[1], i[3])
                if count_activate != 0:
                    count = int(count_activate)
                    await bot.send_message(chat_id=i[0], text=f'Появились номера!\n\n'
                                                              f'Сервис: {Numbers().service_name(i[1])} | {Country().get_country_name(i[2])}\n'
                                                              f'Колличество: {count} шт')
                    async with aiosqlite.connect(self.sql_path) as db:
                        await db.execute(f'DELETE FROM notify_numbers WHERE user_id = "{i[0]}" AND service = "{i[1]}" AND country = "{i[2]}"')
                        await db.commit()

    async def get_wait_sms(self, bot):
        while True:
            async with aiosqlite.connect(self.sql_path) as db:
                select = await db.execute(f'SELECT * FROM wait_sms')
                lists = await select.fetchall()

            for user_id, operation_id, number, service, country, status, times, price, provider in lists:
                print(f'{user_id}, {operation_id}, {number}, {service}, {country}, {status}, {times}, {price}, {provider}')
                if status != 'wait':
                    if provider == 'SMSHub':
                        get_status = await HUB().get_status(operation_id)

                        if 'STATUS_OK:' in get_status:
                            print(f'СМС КОД ХАБ {get_status}')

                            sms_code = await self.sms_code(operation_id, 'SMSHub')
                            if sms_code == 'ERRORS':
                                sms_code = status[10:]


                            if status == 'more_code':
                                await self.write_logs(user_id, operation_id, service, country, number, price, 'more_good')

                                text = more_code_text.format(service=Numbers().service_name(service), country=Country().get_country_name(country),
                                                    number=number, code=sms_code)

                                await bot.send_message(chat_id=user_id, text=text, reply_markup=self.get_wait_menu(service, number, operation_id, price, 'SMSHub'))

                                await self.update_wait_status(operation_id, 'wait')
            
                            elif status == 'first':
                                await self.write_logs(user_id, operation_id, service, country, number, price, 'good')

                                text = good_code_text.format(service=Numbers().service_name(service), country=Country().get_country_name(country),
                                                number=number, code=sms_code)

                                await bot.send_message(chat_id=user_id, text=text, reply_markup=self.get_wait_menu(service, number, operation_id, price, 'SMSHub'))

                                await self.update_wait_status(operation_id, 'wait')
                        else:
                            if status == 'more_code':
                                if time.time() - times >= 1150:
                                    await self.write_logs(user_id, operation_id, service, country, number, price, 'more_bad')

                                    await HUB().set_status(operation_id, 6)
                                    await self.del_wait_sms(operation_id)

                                    try:
                                        await bot.send_message(chat_id=user_id,
                                                    text=f'Номер: {number}\n'
                                                         f'Повторных кодов не было найдено, активация завершена')
                                    except:pass

                            elif status == 'first':
                                if time.time() - times >= 300:
                                    await self.write_logs(user_id, operation_id, service, country, number, price, 'all_bad')
                                        
                                    await self.del_wait_sms(operation_id)
                                    await HUB().set_status(operation_id, 8)
                                    await User(user_id).update_balance(+float(price))

                                    try:
                                        await bot.send_message(chat_id=user_id,
                                                    text=f'Номер: {number}\n'
                                                         f'Код не пришел, вам будут возвращены деньги')
                                    except:pass

                    else:
                        get_status = await Activate().get_status(operation_id)
                        if 'STATUS_OK:' in get_status:
                            print(f'СМС КОД АКТИВЕЙТ {get_status}')
                            sms_code = await self.sms_code(operation_id, 'SMSActivate')

                            if sms_code == 'ERRORS':
                                sms_code = status[10:]

                            if status == 'more_code':
                                await self.write_logs(user_id, operation_id, service, country, number, price, 'more_good')

                                text = more_code_text.format(service=Numbers().service_name(service), country=Country().get_country_name(country),
                                            number=number, code=sms_code)

                                await bot.send_message(chat_id=user_id, text=text, reply_markup=self.get_wait_menu(service, number, operation_id, price, 'SMSActivate'))

                                await self.update_wait_status(operation_id, 'wait')
            
                            elif status == 'first':
                                await self.write_logs(user_id, operation_id, service, country, number, price, 'good')

                                text = good_code_text.format(service=Numbers().service_name(service), country=Country().get_country_name(country),
                                            number=number, code=sms_code)

                                await bot.send_message(chat_id=user_id, text=text, reply_markup=self.get_wait_menu(service, number, operation_id, price, 'SMSActivate'))

                                await self.update_wait_status(operation_id, 'wait')

                        else:
                            if status == 'more_code':
                                if time.time() - times >= 1150:
                                    await self.write_logs(user_id, operation_id, service, country, number, price, 'more_bad')

                                    await Activate().set_status(operation_id, 6)
                                    await self.del_wait_sms(operation_id)

                                    try:
                                        await bot.send_message(chat_id=user_id,
                                               text=f'Номер: {number}\n'
                                                   f'Повторных кодов не было найдено, активация завершена')
                                    except:pass
                            elif status == 'first':
                                if time.time() - times >= 300:
                                    await self.write_logs(user_id, operation_id, service, country, number, price, 'all_bad')

                                    await self.del_wait_sms(operation_id)
                                    await Activate().set_status(operation_id, 8)
                                    await User(user_id).update_balance(+float(price))

                                    try:
                                        await bot.send_message(chat_id=user_id,
                                               text=f'Номер: {number}\n'
                                                   f'Код не пришел, вам будут возвращены деньги')
                                    except:pass
                elif status == 'wait' and (time.time() - times) >= 1150:
                    if provider == 'SMSHub':
                        await HUB().set_status(operation_id, 6)
                    else:
                        await Activate().set_status(operation_id, 6)
                    await self.del_wait_sms(operation_id)
            await asyncio.sleep(0.2)



'''
            info = SMSService(lists)
            async for  i in info:
                i = list(i)
                if i[5] != 'wait':
                    if i[8] == 'SMSHub':
                        await self.get_sms_hub(bot, i[0], i[3], i[4], i[2], i[1], i[7])
                    else:
                        await self.get_sms_activate(bot, i[0], i[3], i[4], i[2], i[1], i[7])
                elif i[5] == 'wait' and (time.time() - i[6]) >= 1150:
                    await bot.send_message(chat_id=i[0], text=f'На номер: {i[2]}, код не пришел')
                    await self.end_service(i[1], i[8])


                
'''
