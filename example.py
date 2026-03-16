import asyncio
import logging

from maxapi import Bot, Dispatcher, F
from maxapi.context import MemoryContext, State, StatesGroup
from maxapi.types import (
    BotStarted,
    Command,
    MessageCreated,
    CallbackButton,
    MessageCallback,
    BotCommand,
)
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from data.config import BOT_TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


start_text = """Пример чат-бота для MAX 💙

Мои команды:

/test очищает ваш контекст
/state или /context показывают ваше контекстное состояние
/data показывает вашу контекстную память
"""


class Form(StatesGroup):
    name = State()
    age = State()
    test = State()


@dp.on_started()
async def _():
    logging.info("Бот стартовал!")


@dp.bot_started()
async def bot_started(event: BotStarted):
    await event.bot.send_message(
        chat_id=event.chat_id, text="Привет! Отправь мне /start"
    )


@dp.message_created(Command("test"))
async def hello(event: MessageCreated, context: MemoryContext):
    await context.set_state(Form.test)
    await event.message.answer(f"Ваш контекст TEST")


@dp.message_created(Command("data"))
async def hello(event: MessageCreated, context: MemoryContext):
    data = await context.get_data()
    await event.message.answer(f"Ваша контекстная память: {str(data)}")


@dp.message_created(Command("context"))
@dp.message_created(Command("state"))
async def hello(event: MessageCreated, context: MemoryContext):
    data = await context.get_state()
    await event.message.answer(f"Ваше контекстное состояние: {str(data)}")


@dp.message_created(Command("start"))
async def hello(event: MessageCreated):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text="Ввести свое имя", payload="btn_1"),
        CallbackButton(text="Ввести свой возраст", payload="btn_2"),
    )
    builder.row(CallbackButton(text="Не хочу", payload="btn_3"))

    await event.message.answer(
        text=start_text,
        attachments=[
            builder.as_markup(),
        ],  # Для MAX клавиатура это вложение,
    )  # поэтому она в списке вложений


@dp.message_callback(F.callback.payload == "btn_1")
async def hello(event: MessageCallback, context: MemoryContext):
    await context.set_state(Form.name)
    await event.message.delete()
    await event.message.answer(f"Отправьте свое имя:")


@dp.message_callback(F.callback.payload == "btn_2")
async def hello(event: MessageCallback, context: MemoryContext):
    await context.set_state(Form.test)
    await event.message.delete()
    await event.message.answer(f"Отправьте ваш возраст:")


@dp.message_callback(F.callback.payload == "btn_3")
async def hello(event: MessageCallback, context: MemoryContext):
    await event.message.delete()
    await event.message.answer(f"Ну ладно 🥲")


@dp.message_created(F.message.body.text, Form.name)
async def hello(event: MessageCreated, context: MemoryContext):
    await context.update_data(name=event.message.body.text)

    data = await context.get_data()

    await event.message.answer(f"Приятно познакомиться, {data['name'].title()}!")


@dp.message_created(F.message.body.text, Form.age, Form.test)
async def hello(event: MessageCreated, context: MemoryContext):
    await context.update_data(age=event.message.body.text)
    corrent_state = await context.get_state()
    if corrent_state is Form.age:
        await event.message.answer(f"Ого! А мне всего пару недель 😁")
    if corrent_state is Form.test:
        await event.message.answer("Сейчас Form.test")


async def main():
    await bot.set_my_commands(
        BotCommand(name="/start", description="Перезапустить бота"),
        BotCommand(name="/clear", description="Очищает ваш контекст"),
        BotCommand(name="/state", description="Показывают ваше контекстное состояние"),
        BotCommand(name="/data", description="Показывает вашу контекстную память"),
        BotCommand(
            name="/context", description="Показывают ваше контекстное состояние"
        ),
    )
    await dp.start_polling(bot)
    # await dp.handle_webhook(
    #     bot=bot,
    #     host='localhost',
    #     port=8080
    # )


if __name__ == "__main__":
    asyncio.run(main())
