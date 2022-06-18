from telethon import TelegramClient
import asyncio, re, requests, datetime, random, json

from telethon import TelegramClient

from data import User, get_user, connect
from utils import config

'''Аккаунт телеграм'''
api_id = 1234
api_hash = '1234'

client = TelegramClient(session="./utils/payments/SmsStore", api_id=api_id, api_hash=api_hash, app_version="10 P (28)",
                        device_model="Iphone", system_version='6.12.0')

client.start()


class BTCPayment():
    def __init__(self):
        self.banker = 'BTC_CHANGE_BOT'
        self.eth_banker = 'ETH_CHANGE_BOT'
        self.chatex = 'Chatex_bot'

    def btc_curs(self):
        '''Курс бтк актуальный '''
        response = requests.get(url='https://blockchain.info/ticker')
        amount = float(response.json()['RUB']['15m'])

        return amount

    def curs_eth(self):
        response = requests.get(url='https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,RUB')
        data = json.loads(response.text)
        USD = data.get('USD')

        return USD

    async def receipt_parser(self, bot, user_id: int, cheque: str):
        '''Проверка, чей чек был отпрвлен, банкир или чатекс '''
        code = re.findall(r'c_\S+', cheque)[0]
        if 'BTC_CHANGE_BOT' in cheque:
            await self.banker_btc(bot, user_id, code)
        elif 'ETH_CHANGE_BOT' in cheque:
            await self.eth_banker_btc(bot, user_id, code)
        else:
            await self.chatex_btc(bot, user_id, code)


    async def banker_btc(self, bot, user_id: int, cheque: str):
        await client.send_message(self.banker, f'/start {cheque}')
        msg_bot = await self.get_last_message_banker()

        if 'Вы получили' in msg_bot:
            btc = msg_bot.replace('(', '').replace(')', '').split(' ')
            amount = round(float(btc[2]) * self.btc_curs())
            money = await self.referals(user_id, amount)
            await User(user_id).update_balance(money)

            await self.deposit_logs(user_id, 'banker', amount)
            await bot.send_message(chat_id=user_id, text=f'Получено + {money} RUB')
            await bot.send_message(chat_id=config.config('admin_group'),
                                           text=f'<b>♻️ Пришло пополнение Banker!</b>\n\n'
                                                f'<b>🧑🏻‍🔧 От:</b> @{User(user_id).username} | {user_id}\n\n'
                                                f'<b>💰 Сумма:</b> {amount} RUB')

        else:
            await bot.send_message(chat_id=user_id, text=msg_bot)


    async def chatex_btc(self, bot, user_id: int, cheque: str):
        await client.send_message(self.chatex, f'/start {cheque}')
        msg_bot = await self.get_last_message_chatex()

        if 'Ваучер на сумму' in msg_bot:
            money = re.findall("\d.\d+ BTC", msg_bot)[0]
            if money.split(" ")[1] == 'BTC':
                btc = re.findall("\d.\d+", money)[0]
                amount = round(float(btc) * self.btc_curs())
                money = await self.referals(user_id, amount)
                await User(user_id).update_balance(money)

                await self.deposit_logs(user_id, 'chatex', amount)
                await bot.send_message(chat_id=user_id, text=f'Получено + {money} RUB')
                await bot.send_message(chat_id=config.config('admin_group'),
                                           text=f'<b>♻️ Пришло пополнение Chatex!</b>\n\n'
                                                f'<b>🧑🏻‍🔧 От:</b> @{User(user_id).username} | {user_id}\n\n'
                                                f'<b>💰 Сумма:</b> {amount} RUB')

            else:
                await bot.send_message(chat_id=user_id, text='Упс, чек был не BTC, деньги я схавал')

        else:
            await bot.send_message(chat_id=user_id, text=msg_bot)

    async def eth_banker_btc(self, bot, user_id: int, cheque: str):
        await client.send_message(self.eth_banker, f'/start {cheque}')
        msg_bot = await self.get_last_message_eth()

        if 'Вы получили' in msg_bot:
            eth = msg_bot.replace('(', '').replace(')', '').split(' ')
            if float(eth[4]) >= 90:
                amount = round(float(eth[2]) * self.curs_eth())
                money = await self.referals(user_id, amount)
                await User(user_id).update_balance(money)

                await self.deposit_logs(user_id, 'banker', amount)
                await bot.send_message(chat_id=user_id, text=f'Получено + {money} RUB')
                await bot.send_message(chat_id=config.config('admin_group'),
                                        text=f'<b>♻️ Пришло пополнение ETH Banker!</b>\n\n'
                                             f'<b>🧑🏻‍🔧 От:</b> @{User(user_id).username} | {user_id}\n\n'
                                             f'<b>💰 Сумма:</b> {amount} RUB')
            else:
                await bot.send_message(chat_id=user_id, text=f'Сумма пополнения, меньше 100 рублей (получено: {eth[4]}')
        else:
            await bot.send_message(chat_id=user_id, text=msg_bot)


    async def deposit_logs(self, user_id: int, types: str, amount: float):
        conn, cursor = connect()

        logs = [random.randint(11111, 99999), user_id, types, amount, datetime.datetime.now()]
        sql = 'INSERT INTO deposit_logs VALUES (?,?,?,?,?)'
        cursor.execute(sql, logs)
        conn.commit()

    async def referals(self, user_id: int, amount: float):
        user = User(user_id)
        
        if user.who_invite != 0:
            if await get_user(user.who_invite) != False:

                percent = config.config("ref_percent")
                ref_money = amount / 100 * float(percent)
                money = amount - ref_money

                referal =  User(user.who_invite)
                await referal.update_balance(ref_money)
                await referal.referals_profit(ref_money)
            else:
                money = amount
        else:
            money = amount

        return money
   
    async def get_last_message_banker(self) -> str:
        while True:
            message = (await client.get_messages("BTC_CHANGE_BOT", limit=1))[0]
            if message.message.startswith("Приветствую,"):
                await asyncio.sleep(0.5)
                continue
            if message.from_id is not None:
                me = await client.get_me()
                if message.from_id.user_id == me.id:
                    await asyncio.sleep(0.5)
                    continue
            else:
                return message.message

    async def get_last_message_chatex(self) -> str:
        while True:
            message = (await client.get_messages("Chatex_bot", limit=1))[0]
            if message.from_id is not None:
                me = await client.get_me()
                if message.from_id.user_id == me.id:
                    await asyncio.sleep(0.5)
                    continue
            else:
                return message.message

    async def get_last_message_eth(self) -> str:
        while True:
            message = (await client.get_messages(self.eth_banker, limit=1))[0]
            if message.message.startswith("Приветствую,"):
                await asyncio.sleep(0.5)
                continue
            if message.from_id is not None:
                me = await client.get_me()
                if message.from_id.user_id == me.id:
                    await asyncio.sleep(0.5)
                    continue
            else:
                return message.message
    

