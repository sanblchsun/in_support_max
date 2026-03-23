import asyncio
import logging

from maxapi import Bot, Dispatcher
from data.config import BOT_TOKEN

# Кнопки
from maxapi.types import (
    ChatButton, 
    LinkButton, 
    CallbackButton, 
    RequestGeoLocationButton, 
    MessageButton, 
    ButtonsPayload, # Для постройки клавиатуры без InlineKeyboardBuilder
    RequestContactButton, 
    OpenAppButton, 
)

from maxapi.types import (
    MessageCreated, 
    MessageCallback, 
    MessageChatCreated,
    CommandStart, 
    Command
)

from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message_created()
async def builder_process(event: MessageCreated):

    buttons = [
        [LinkButton(text="Сайт", url="https://example.com")],
        [CallbackButton(text="Callback", payload="some_data")]
    ]
    payload = ButtonsPayload(buttons=buttons).pack()
    await event.message.answer(
        text='Вот клавиатура',
        attachments=[payload]
    )
 

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())