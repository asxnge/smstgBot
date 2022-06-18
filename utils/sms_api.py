from aiogram import types
from random import randint
from aiosqlite import connect

from data import User
from utils import config, misc


class Numbers():
    def __init__(self):
        self.sql_path = './data/database.db'
        self.favorites = ['av', 'wa', 'vi', 'vk', 'tg',
                          'sn', 'ok', 'ya', 'go', 'ym', 'ig', 'ot']
        self.black_list = ['ma', 'fd', 'mg', 'md']
        self.service_names = misc.service
        self.service = misc.country

    def service_name(self, code):
        name = self.service_names.get(code)
        return name

    def get_service(self, country):
        service = self.service.get(country)
        lists = list(service.keys())

        return lists

    async def get_service_price(self, country, service):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM service WHERE service_code = ? AND  country = ?', [service, country])
            info = await select.fetchone()
            await select.close()

        price = info[4]

        return price

    async def get_services(self, country, service):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM service WHERE service_code = ? AND  country = ?', [service, country])

            service = await select.fetchall()
            await select.close()

        return service


    async def get_buy_menu(self, user_id, country, service):
        operator = User(user_id).operator
        info = await FavoriteSerivice().check_favorite(user_id, country, service)

        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton(
                text='📩 Получить код', callback_data=f'sms_service:{country}:{service}:{operator}')
        )

        if info == None:
            markup.add(
                types.InlineKeyboardButton(text='⭐️ Добавить в Избранное', callback_data=f'add_favorite:{country}:{service}'))
        else:
            markup.add(types.InlineKeyboardButton(
                text='⭐️ Удалить из Избраного', callback_data=f'del_favorite:{country}:{service}'))
        markup.add(
            types.InlineKeyboardButton(
                text='🔙 Назад', callback_data=f'service_pages:{country}'),
            types.InlineKeyboardButton(
                text='🖥 Меню', callback_data=f'to_menu')
        )

        return markup

    def service_menu(self, country, page_number=1):
        service = self.get_service(country)

        numbers = []
        x = 1
        for i in service:
            if len(i) < 3:
                if i not in self.black_list:
                    if i in self.favorites:
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
                    types.InlineKeyboardButton(text=self.service_name(
                        pages[page_number-1][x1]), callback_data=f'buy_service:{country}:{pages[page_number-1][x1]}'),
                    types.InlineKeyboardButton(text=self.service_name(
                        pages[page_number-1][x2]), callback_data=f'buy_service:{country}:{pages[page_number-1][x2]}'),
                    types.InlineKeyboardButton(text=self.service_name(
                        pages[page_number-1][x3]), callback_data=f'buy_service:{country}:{pages[page_number-1][x3]}'),
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
                text='⭐️ Избранное', callback_data='favorite_service')
        )
        markup.add(
            types.InlineKeyboardButton(
                text='ᐊ', callback_data=f'service_page:{country}:{previous_page_number}'),
            types.InlineKeyboardButton(
                text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'),
            types.InlineKeyboardButton(
                text='ᐅ', callback_data=f'service_page:{country}:{next_page_number}'),
            types.InlineKeyboardButton(
                text='🔚 Назад', callback_data='to_menu'),
        )

        return markup


class Country():
    def __init__(self):
        self.api = config.config("api_smsactivate")
        self.base = misc.countries

    def get_country_name(self, code):
        return self.base.get(code)

    def country_menu(self, page_number=1):
        country = list(self.base.keys())
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
                    types.InlineKeyboardButton(text=self.get_country_name(
                        pages[page_number-1][x1]), callback_data=f'country:{pages[page_number-1][x1]}'),
                    types.InlineKeyboardButton(text=self.get_country_name(
                        pages[page_number-1][x2]), callback_data=f'country:{pages[page_number-1][x2]}'),
                    types.InlineKeyboardButton(text=self.get_country_name(
                        pages[page_number-1][x3]), callback_data=f'country:{pages[page_number-1][x3]}'),
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
                text='Выбрать оператора', callback_data=f'get_operators'),
        )
        markup.add(
            types.InlineKeyboardButton(
                text='ᐊ', callback_data=f'page:{previous_page_number}'),
            types.InlineKeyboardButton(
                text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'),
            types.InlineKeyboardButton(
                text='ᐅ', callback_data=f'page:{next_page_number}'),
            types.InlineKeyboardButton(
                text='🔚 Назад', callback_data='to_menu'),
        )

        return markup


class Operator():
    def __init__(self):
        self.operators = misc.operators

    def get_operator_name(self, country, code):
        index = self.operators.get(f"{country}")
        operator = index.get(code)

        return operator

    def operator_menu(self, country):
        index = self.operators.get(f"{country}")
        lists = list(index.keys())

        markup = types.InlineKeyboardMarkup(row_width=2)
        x1 = 0
        x2 = 1
        for i in range(len(lists)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text=self.get_operator_name(
                        country, lists[x1]), callback_data=f'set_operator:{lists[x1]}'),
                    types.InlineKeyboardButton(text=self.get_operator_name(
                        country, lists[x2]), callback_data=f'set_operator:{lists[x2]}'),
                )
                x1 += 2
                x2 += 2
            except:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text=self.get_operator_name(
                            country, lists[x1]), callback_data=f'set_operator:{lists[x1]}')
                    )
                    break
                except:
                    pass

        markup.add(
            types.InlineKeyboardButton(
                text='🔚 Назад', callback_data='to_menu'),
        )

        return markup


class FavoriteSerivice():
    def __init__(self) -> None:
        self.sql_path = './data/database.db'

    async def add_favorite(self, user_id, country, service):
        async with connect(self.sql_path) as db:
            await db.execute('INSERT INTO favorite VALUES (?,?,?,?)', 
                    [f'f_{randint(1111, 9999)}', user_id, country, service])
            await db.commit()

    async def del_favorite(self, user_id, country, service):
        async with connect(self.sql_path) as db:
            await db.execute('DELETE FROM favorite WHERE user_id = ? AND country = ? AND service = ?',
                            [user_id, country, service])
            await db.commit()

    async def favorite_service(self, user_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM favorite WHERE user_id = ?', [user_id])
            info = await select.fetchone()
            await select.close()
        
        return info


    async def check_favorite(self, user_id, country, service):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM favorite WHERE user_id = ? AND country = ? AND service = ?',
                            [user_id, country, service])
            favorite = await select.fetchone()
            await select.close()
        
        return favorite

    async def get_menu(self, user_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM favorite WHERE user_id = ?', [user_id])
            favorite = await select.fetchall()
            await select.close()

        favorite = list(favorite)

        if len(favorite) > 0:
            markup = types.InlineKeyboardMarkup(row_width=2)
            x1 = 0
            x2 = 1
            country = Country()
            numbers = Numbers()
            for i in range(len(favorite)):
                try:
                    markup.add(
                        types.InlineKeyboardButton(
                            text=f'{numbers.service_name(favorite[x1][3])} | {country.get_country_name(favorite[x1][2])}', callback_data=f'buy_service:{favorite[x1][2]}:{favorite[x1][3]}'),
                        types.InlineKeyboardButton(
                            text=f'{numbers.service_name(favorite[x2][3])} | {country.get_country_name(favorite[x2][2])}', callback_data=f'buy_service:{favorite[x1][2]}:{favorite[x2][3]}')
                    )
                    x1 += 2
                    x2 += 2
                except:
                    try:
                        markup.add(
                            types.InlineKeyboardButton(
                                text=f'{numbers.service_name(favorite[x1][3])} | {country.get_country_name(favorite[x1][2])}', callback_data=f'buy_service:{favorite[x1][2]}:{favorite[x1][3]}')
                        )
                        break
                    except:
                        pass
            markup.add(
                types.InlineKeyboardButton(
                    text='🔚 Назад', callback_data='to_menu')
            )

            return markup
        else:
            return False
