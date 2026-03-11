import asyncio
from loguru import logger
from loader import dp, bot

# строку не удалять, она работает
import middlewares, filters, handlers
from states.timeout_worker import fsm_timeout_worker

# from utils.notify_admins import on_startup_notify
# from utils.set_bot_commands import set_default_commands


async def on_startup():
    logger.info("Запуск БОТа")
    await bot.delete_webhook()
    logger.info("Бот запущен")
    asyncio.create_task(fsm_timeout_worker())
    await dp.start_polling(bot)
    # # Устанавливаем дефолтные команды
    # await set_default_commands(dispatcher)

    # # Уведомляет про запуск
    # await on_startup_notify(dispatcher)


if __name__ == "__main__":
    asyncio.run(on_startup())
