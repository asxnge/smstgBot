from aiosqlite import connect
from aiogram import types

from utils.sms_api import Country, Numbers
from utils.activate import Activate


class AdminRent():
    def __init__(self):
        self.sql_path = './data/database.db'

    def adm_rent_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(
                text='4 часа', callback_data='adm_rent_edit:4'),
            types.InlineKeyboardButton(
                text='12 часов', callback_data='adm_rent_edit:12'),
            types.InlineKeyboardButton(
                text='24 часа', callback_data='adm_rent_edit:24'),
            types.InlineKeyboardButton(
                text='3 дня', callback_data='adm_rent_edit:72')
        )
        markup.add(
            types.InlineKeyboardButton(
                text='7 дней', callback_data='adm_rent_edit:168'),
            types.InlineKeyboardButton(
                text='14 дней', callback_data='adm_rent_edit:336'),
        )
        markup.add(
            types.InlineKeyboardButton(
                text='🔚 Закрыть', callback_data='to_closed')
        )

        return markup

class AdminService():
    def __init__(self):
        self.sql_path = './data/database.db'
        self.country = Country().base

    def country_name(self, code):
        name = self.country.get(code)

        return name

    def country_adm_menu(self, page_number=1):
        country = list(self.country.keys())
        rows = 15
        page = []
        pages = []
        for i in country:
            page.append(i)
            if len(page) == rows:
                pages.append(page)
                page = []

        if str(len(country) / rows) not in range(30):
            pages.append(page)

        markup = types.InlineKeyboardMarkup(row_width=3)
        x1 = 0
        x2 = 1
        x3 = 2
        for i in range(int(len(pages[page_number-1]) / 3)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text=self.country_name(
                        pages[page_number-1][x1]), callback_data=f'adm_country:{pages[page_number-1][x1]}'),
                    types.InlineKeyboardButton(text=self.country_name(
                        pages[page_number-1][x2]), callback_data=f'adm_country:{pages[page_number-1][x2]}'),
                    types.InlineKeyboardButton(text=self.country_name(
                        pages[page_number-1][x3]), callback_data=f'adm_country:{pages[page_number-1][x3]}'),
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
            next_page_number = next_page_number-1

        markup.add(
            types.InlineKeyboardButton(
                text='ᐊ', callback_data=f'adm_page:{previous_page_number}'),
            types.InlineKeyboardButton(
                text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'),
            types.InlineKeyboardButton(
                text='ᐅ', callback_data=f'adm_page:{next_page_number}'),
            types.InlineKeyboardButton(
                text='💢 Закрыть', callback_data='to_closed'),
        )

        return markup

    def service_menu(self, country, page_number=1):
        service = Numbers().get_service(country)

        numbers = []
        x = 1
        for i in service:
            if len(i) < 3:
                if i not in Numbers().black_list:
                    if i in Numbers().favorites:
                        numbers.insert(x, i)
                        x += 1
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

        markup = types.InlineKeyboardMarkup(row_width=3)
        x1 = 0
        x2 = 1
        x3 = 2
        for i in range(int(len(pages[page_number-1]) / 3)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text=Numbers().service_name(
                        pages[page_number-1][x1]), callback_data=f'adm_service:{country}:{pages[page_number-1][x1]}'),
                    types.InlineKeyboardButton(text=Numbers().service_name(
                        pages[page_number-1][x2]), callback_data=f'adm_service:{country}:{pages[page_number-1][x2]}'),
                    types.InlineKeyboardButton(text=Numbers().service_name(
                        pages[page_number-1][x3]), callback_data=f'adm_service:{country}:{pages[page_number-1][x3]}'),
                )

                x1 += 3
                x2 += 3
                x3 += 3

            except:pass

        previous_page_number = page_number+1 if page_number == 1 else page_number-1
        next_page_number = page_number + \
            1 if len(pages) > page_number else page_number
        if page_number == len(pages):
            previous_page_number = previous_page_number
            next_page_number = 1

        markup.add(
            types.InlineKeyboardButton(
                text='ᐊ', callback_data=f'adm_service_page:{country}:{previous_page_number}'),
            types.InlineKeyboardButton(
                text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'),
            types.InlineKeyboardButton(
                text='ᐅ', callback_data=f'adm_service_page:{country}:{next_page_number}'),
            types.InlineKeyboardButton(
                text='💢 Закрыть', callback_data='to_closed'),
        )

        return markup

    async def get_percent(self, country, service):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM service WHERE service_code = ? AND  country = ?', [service, country])
            info = await select.fetchone()
            await select.close()
        
        percent = info[6]
        return percent
    
    async def update_price(self, country, service, price):
        async with connect(self.sql_path) as db:
            sql = 'UPDATE service SET price = ? WHERE service_code = ? AND country = ?'
            await db.execute(sql, [price, service, country])
            await db.commit()
        
    async def update_priceservice(self, country, service, price):
        async with connect(self.sql_path) as db:
            sql = 'UPDATE service SET price_service = ? WHERE service_code = ? AND country = ?'
            await db.execute(sql, [price, service, country])
            await db.commit()

    async def update_percent(self, country, service, percent):
        async with connect(self.sql_path) as db:
            sql = 'UPDATE service SET percent = ? WHERE service_code = ? AND country = ?'
            await db.execute(sql, [percent, service, country])
            await db.commit()
    
    async def update_percent_service(self, country, service, percent):
        price = await Activate().get_price(country, service)
        if price != 0:
            await self.update_percent(country, service, percent)
            await self.update_priceservice(country, service, price)
            new_price = float(price) / 100 * int(percent) + float(price)

            await self.update_price(country, service, new_price)
        else:
            new_price = 0
        
        return new_price, price
