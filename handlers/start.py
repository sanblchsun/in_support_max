# handlers/start.py
import random

from maxapi.context import MemoryContext

from base.sqlighter import SQLighter
from loader import dp, bot
from utils.timeout_manager import set_timeout
from utils.message_manager import add_message
from keyboards.inline.buttons import request_delete_with_data, request_or_reject
from maxapi.types import Command, MessageCreated
from maxapi.types import InputMedia
from loguru import logger

from states.forms import Form


async def send_photo(chat_id: int, path: str):
    photo = InputMedia(path)
    return await bot.send_message(chat_id=chat_id, attachments=[photo])


@dp.message_created(Command("start"))
async def bot_start(event: MessageCreated, context: MemoryContext):

    await context.clear()

    await context.set_state(Form.beginning)

    await event.message.answer(
        "Начат процесс подачи заявки. "
        "Если он не будет завершён за 30 минут, "
        "то произойдет автоматическая отмена."
    )

    chat_id = event.message.recipient.chat_id
    user_id = event.from_user.user_id  # type: ignore

    await set_timeout(event, context, bot, 18000)

    sql = SQLighter("base/db.db")
    client = sql.get_client(user_id)

    # отправляем фото
    try:
        await send_photo(chat_id, f"img/supp{random.randint(1,5)}.jpeg")  # type: ignore
    except FileNotFoundError:
        ...

    # ---------- клиент уже есть ----------

    if client:
        c = client[0]

        msg = await event.message.answer(
            f"Привет, {event.from_user.full_name}!\n\n"  # type: ignore
            f"Ваши данные для автозаполнения формы:\n\n"
            f"ФИО: {c[1]}\n"
            f"Организация: {c[2]}\n"
            f"e-mail: {c[3]}\n"
            f"телефон: {c[4]}",
            attachments=[request_delete_with_data()],
        )

        await add_message(context, msg)

        msg1 = await event.message.answer("Расскажите - что у вас случилось?")
        await add_message(context, msg1)

        await context.set_state(Form.description)

        await context.update_data(
            full_name=c[1],
            firma=c[2],
            e_mail=c[3],
            telefon=c[4],
            message_for_edit=msg,
        )

    # ---------- новый пользователь ----------

    else:
        msg1 = await event.message.answer(
            """Уважаемый пользователь, вас приветствует MAX-бот ИИС!

Прошу Вас ответить на несколько вопросов,
которые мне необходимо задать для отправки
Вашей заявки в техническую поддержку.""",
            attachments=[request_or_reject()],
        )

        await add_message(context, msg1)
        await context.set_state(Form.beginning)
