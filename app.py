# app.py
import asyncio
from loguru import logger
from maxapi.types import BotCommand
from loader import dp, bot
from base.mysqlrequests import init_db, close_db
from data import config

# строку не удалять, она работает
import handlers


async def on_startup():
    logger.info("Запуск БОТа")
    await bot.delete_webhook()
    logger.info("Бот запущен")
    # await init_db(
    #     host=config.HOST,
    #     port=config.PORT,
    #     user=config.USER,
    #     password=config.PASSWORD,
    #     database=config.DATABASE,
    # )
    await dp.start_polling(bot)
    
async def on_shutdown():
    await close_db()


if __name__ == "__main__":
    asyncio.run(on_startup())
