# app.py
import asyncio
from loguru import logger
from maxapi.types import BotCommand
from loader import dp, bot
from base.mysqlrequests import init_db, close_db

# строку не удалять, она работает
import handlers


async def on_startup():
    logger.info("Запуск БОТа")
    await bot.delete_webhook()
    logger.info("Бот запущен")
    await init_db(
        host="localhost",   # 👈 имя контейнера
        port=3306,
        user="root",
        password="Ghjuhtcc",
        database="requests_from_user",
    )
    await dp.start_polling(bot)
    
async def on_shutdown():
    await close_db()


if __name__ == "__main__":
    asyncio.run(on_startup())
