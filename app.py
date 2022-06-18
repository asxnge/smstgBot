from aiogram import executor, types
import asyncio

from loader import bot, vip
import handlers, middlewares
from utils import logger, SMSService, RentBuyer, QiwiPay
from utils.parser import check_prices

async def startup(dp):
    asyncio.create_task(SMSService().get_wait_sms(dp.bot))
    asyncio.create_task(handlers.admin.admin_sending.sending_checked(10))

    asyncio.create_task(RentBuyer().select_sms(dp.bot))
    asyncio.create_task(QiwiPay().wait_pays_qiwi(dp.bot, 10))
    asyncio.create_task(check_prices(dp.bot))
    asyncio.create_task(SMSService().check_count_numbers(dp.bot))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(SMSService().get_wait_sms(bot))
    loop.create_task(handlers.admin.admin_sending.sending_checked(10))
    loop.create_task(RentBuyer().select_sms(bot))
    loop.create_task(SMSService().check_count_numbers(bot))

    logger.debug('SMS | Started')
    executor.start_polling(vip, skip_updates=True, on_startup=startup)
