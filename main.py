# main.py
import asyncio
import config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.dispatcher.router import Router
from aiogram.enums import ParseMode
from handlers import setup_handlers
from db.database import create_tables
# from keyboards.admin import  *

async def main():
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    main_router = Router()

    await create_tables()
    setup_handlers(main_router)
    dp.include_router(main_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
