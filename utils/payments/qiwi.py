from aiosqlite import connect
from aiohttp import ClientSession
import datetime, requests, time, json
import asyncio, ssl, certifi
from random import randint
from aiogram import types
from qiwi_payments.kassa import QiwiKassa
from data import User, functions as func
from utils import config

class QiwiPay():
    def __init__(self):
        self.sql_path = './data/database.db'
        self.token = config.config("qiwi_token")
        self.phone = config.config("qiwi_number")

    async def get_payments(self):
        db = await connect(self.sql_path)
        select = await db.execute('SELECT * FROM wait_qiwi')
        payments = await select.fetchall()

        await select.close()
        await db.close()
        
        return payments

    async def delete_pays(self, user_id):
        db = await connect(self.sql_path)
        await db.execute('DELETE FROM wait_qiwi WHERE user_id = ?', [user_id])
        await db.commit()
        await db.close()

    async def deposit_logs(self, user_id: int, types: str, amount: float):
        db = await connect(self.sql_path)
        logs = [randint(11111, 99999), user_id, types, amount, datetime.datetime.now()]

        await db.execute('INSERT INTO deposit_logs VALUES (?,?,?,?,?)', logs)
        await db.commit()
        await db.close()

    async def deposit_qiwi(self, user_id):
        db = await connect(self.sql_path)
        select = await db.execute('SELECT * FROM wait_qiwi WHERE user_id = ?', [user_id])
        user = await select.fetchall()

        user = list(user)
        if len(user) > 0:
            date = datetime.datetime.strptime(user[0][2], '%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(minutes=15)
            if date < datetime.datetime.now():
                await db.execute('DELETE FROM wait_qiwi WHERE user_id = ?', [user_id])
                await db.commit()

                code = randint(11111, 99999)

                await db.execute('INSERT INTO wait_qiwi VALUES (?,?,?)', [user_id, code, datetime.datetime.now()])
                await db.commit()
            else:
                code = user[0][1]
        else:
            code = randint(11111, 99999)
            await db.execute('INSERT INTO wait_qiwi VALUES (?,?,?)', [user_id, code, datetime.datetime.now()])
            await db.commit()
            
        await select.close()
        await db.close()
        
        url = f'https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={self.phone}&amountFraction=0&extra%5B%27comment%27%5D={code}&currency=643&&blocked[0]=account&&blocked[1]=comment'

        return url, code, self.phone

    async def get_history(self):
        try:
            headers = {
                'Authorization': 'Bearer {}'.format(self.token)
            }
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            async with ClientSession(headers=headers) as session:
                params = {
                    'rows': '10'
                }
                url = f'https://edge.qiwi.com/payment-history/v1/persons/{self.phone}/payments'
                async with session.get(url=url, params=params, ssl_context=ssl_context) as response:
                    data = await response.text()
                    req = json.loads(data)
            history = req['data']
        except:
            history = None

        return history

    async def wait_pays_qiwi(self, bot, wait_for):
        while True:
            data = await self.get_history()
            if data != None:    
                lists_pays = await self.get_payments()

                for i in range(len(data)):
                    for code in lists_pays:
                        date = datetime.datetime.strptime(code[2], '%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(minutes=15)

                        if date < datetime.datetime.now():
                            await self.delete_pays(code[0])

                        elif data[i]['comment'] == code[1]:
                            if str(data[i]['sum']['currency']) == '643':
                                amount = float(data[i]['sum']['amount'])

                                await User(code[0]).update_balance(amount)

                                await self.deposit_logs(code[0], 'qiwi', amount)

                                await bot.send_message(chat_id=code[0], text=f'✅ Вам начислено + {amount}')

                                await bot.send_message(chat_id=config.config('admin_group'),
                                                text=f'<b>♻️ Пришло пополнение Qiwi!</b>\n\n'
                                                    f'<b>🧑🏻‍🔧 От:</b> @{User(code[0]).username} | {code[0]}\n\n'
                                                    f'<b>💰 Сумма:</b> {amount} RUB')
                            
                                await self.delete_pays(code[0])

            await asyncio.sleep(wait_for)
