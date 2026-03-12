# app.py
import asyncio
from loguru import logger
from loader import dp, bot

# строку не удалять, она работает
import middlewares, handlers



async def on_startup():
    logger.info("Запуск БОТа")
    await bot.delete_webhook()
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(on_startup())
