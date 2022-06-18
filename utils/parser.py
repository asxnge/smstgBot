from aiosqlite import connect
import asyncio
from aiogram import types

from loader import bot
from utils import config, Numbers, Country, misc, Activate



async def check_prices(bot):
    '''SMS activation and rental price parser'''
    while True:
        chat_id = config.config("admin_owner").split(":")[0]
        sql_path = './data/database.db'

        service = list(misc.service.keys())
        country = list(Country().base.keys())

        for i in country:
            for number in service:
                print(f'Country: {i}, Service: {number}')
                price = await Numbers().get_services(i, number)
                if price != None:

                    for info in price:
                        percent = int(info[6])
                        price_service = await Activate().get_price(i, number)

                        if price_service != 0 and price_service > float(info[5]):
                            current_price = float(info[5])
                            service_price = float('{:.2f}'.format(price_service))

                            #if current_price != service_price:
                            print(f'Service price {service_price} | current_price {current_price}')
                            async with connect(sql_path) as db:
                                await db.execute('UPDATE service SET price_service = ? WHERE service_code = ? AND country = ?',
                                            [service_price, number, i])
                                await db.commit()

                            
                            await bot.send_message(chat_id=chat_id,
                                                    text=f'Изменена цена на сервисе: {Numbers().service_name(number)}\n'
                                                       f'Новая цена на сервисе: {service_price}\n'
                                                       f'Старая цена на сервисе: {current_price}\n'
                                                       f'Страна: {Country().get_country_name(i)}')

                            price_bot = float(info[4])
                            new_price = service_price / 100 * int(percent) + service_price
                            print(f'UP_AMOUNT: {new_price}')

                            if price_bot != new_price:
                                async with connect(sql_path) as db:
                                    await db.execute('UPDATE service SET price = ? WHERE service_code = ? AND country = ?',
                                            [new_price, number, i])
                                    await db.commit()

                                
                                await bot.send_message(chat_id=chat_id,
                                                        text=f'Изменена цена в боте!\n'
                                                           f'Cервис: {Numbers().service_name(number)}\n'
                                                           f'Cтрана: {Country().get_country_name(i)}\n'
                                                           f'Cмена цены: была {price_bot} RUB cтала {new_price} RUB')
        await asyncio.sleep(86400)