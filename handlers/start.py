# handlers/start.py
import random

from base.sqlighter import SQLighter
from loader import dp, bot
from states.context import FSMContext
from keyboards.inline.buttons import request_delete_with_data
from maxapi.types import Attachment, BotStarted, Command, MessageCreated
from maxapi.types import InputMedia
from loguru import logger

from states.forms import Form


async def send_photo(chat_id: int, path: str):
    photo = InputMedia(path)
    return await bot.send_message(chat_id=chat_id, attachments=[photo])


@dp.message_created(Command("start"))
async def bot_start(event: MessageCreated, state: FSMContext):

    await state.set_state(Form.BEGINNING)

    await event.message.answer(
        "Начат процесс подачи заявки. "
        "Если он не будет завершён за 30 минут, "
        "то произойдет автоматическая отмена."
    )

    chat_id = event.message.recipient.chat_id
    user_id = event.from_user.user_id  # type: ignore

    await state.set_timeout(100)

    await state.update_data(
        dist_url_and_namefile={}, list_photo_path=[], send_yes_no=True
    )

    sql = SQLighter("base/db.db")
    client = sql.get_client(user_id)

    # отправляем фото
    try:
        msg0 = await send_photo(chat_id, f"img/supp{random.randint(1,5)}.jpeg")  # type: ignore
        await state.add_message(msg0)
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

        await state.add_message(msg)

        await event.message.answer("Расскажите - что у вас случилось?")

        await state.set_state(Form.DESCRIPTION)

        await state.update_data(
            full_name=c[1],
            firma=c[2],
            e_mail=c[3],
            telefon=c[4],
        )

        await event.message.delete()

    # ---------- новый пользователь ----------

    else:
        msg1 = await event.message.answer(
            """Уважаемый пользователь, вас приветствует ТГ-бот ИИС!

Прошу Вас ответить на несколько вопросов,
которые мне необходимо задать для отправки
Вашей заявки в техническую поддержку.""",
            attachments=[request_delete_with_data()],
        )

        await state.add_message(msg1)
        await state.set_state(Form.BEGINNING)
