import sqlite3
from aiosqlite import connect
from datetime import datetime, date

class User():
    def __init__(self, user_id):
        self.sql_path = './data/database.db'
        conn = sqlite3.connect(self.sql_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE user_id = ?', [user_id])
        user = cursor.fetchone()

        self.user_id = user[0]
        self.username = user[1]
        self.balance = user[2]
        self.country = user[3]
        self.operator = user[4]
        self.who_invite = user[5]
        self.date = user[6]
        self.ban = user[7]

    async def update_balance(self, value):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE users SET balance = ? WHERE user_id = ?', [float(self.balance) + float(value), self.user_id])
            await db.commit()
        
        return True

    async def up_ban(self, value):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE users SET ban = ? WHERE user_id = ?', [value, self.user_id])
            await db.commit()
        
        return True

    async def up_balance(self, value):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE users SET balance = ? WHERE user_id = ?', [value, self.user_id])
            await db.commit()
        
        return True

    async def up_country(self, value):
        async with connect(self.sql_path) as db:
            await db.execute(f'UPDATE users SET country = ? WHERE user_id = ?', [value,self.user_id])
            await db.commit()
        
        return True

    async def up_operator(self, value):
        async with connect(self.sql_path) as db:
            await db.execute(f'UPDATE users SET operator = ? WHERE user_id = ?', [value, self.user_id])
            await db.commit()
        
        return True

    def get_days(self):
        join_time = self.date[:10].split('-')
        pars_time = date(int(join_time[0]), int(join_time[1]), int(join_time[2]))
        today = date.today()
        delta = today - pars_time
        day = str(delta).split()[0]
        if day.split(':')[0] == '0':
            day = 1
        
        return day

    async def referals_profit(self, amount):
        logs = [self.user_id, amount, datetime.now()]
        async with connect(self.sql_path) as db:
            await db.execute('INSERT INTO refferal_logs VALUES (?,?,?)', logs)
            await db.commit()
        
        return True

async def first_join(user_id, username, code):
    status, invite = False, 0
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT * FROM users WHERE user_id = ?', [user_id])
        row = await select.fetchall()

        who_invite = code[7:]

        if who_invite == '':
            who_invite = 0
        
        select_invite = await db.execute('SELECT * FROM users WHERE user_id = ?', [who_invite])
        invite = await select_invite.fetchall()
        if len(list(invite)) == 0:
            who_invite = 0

        if len(list(row)) == 0:
            users = [user_id, f'{username}', 0, 0, 'any', who_invite, datetime.now(), 'no']
            await db.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?,?)', users)
            await db.commit()

            status, invite = True, who_invite

    return status, invite


async def get_user(user_id) -> bool:
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT * FROM users WHERE user_id = ?', [user_id])
        row = await select.fetchall()

        if len(list(row)) > 0:
            status = True
        else:
            status = False

    return status

async def amount_referals(user_id):
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT * FROM users WHERE who_invite = ?', [user_id])
        check = await select.fetchall()
    
    referals = len(list(check))

    return referals