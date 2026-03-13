# handlers/users/start.py
import random

from base.sqlighter import SQLighter
from loader import dp, bot
from states.context import FSMContext
from states.user_state import UserState

from keyboards.inline.buttons import request_delete_with_data

# 1. FIX: Import InputMediaType from the library's enums
from maxapi.types import Attachment, BotStarted, Command, MessageCreated
from maxapi.types import InputMedia


async def send_photo(chat_id: int, path: str):
    photo = InputMedia(path)
    return await bot.send_message(chat_id=chat_id, attachments=[photo])


# REVERT TO THIS SIGNATURE: The dispatcher will now correctly inject the state.
@dp.message_created(Command("start"))
async def bot_start(event: MessageCreated, state: FSMContext):

    chat_id = event.message.recipient.chat_id
    user_id = event.message.sender.user_id  # type: ignore

    if chat_id is None:
        return

    # --- The rest of your function code remains the same ---
    # It will now work correctly.
    await state.set_state(UserState.WAITING)

    await event.message.answer(
        "Начат процесс подачи заявки. "
        "Если он не будет завершён за 30 минут, "
        "то произойдет автоматическая отмена."
    )

    await state.set_timeout(100)

    await state.update_data(
        dist_url_and_namefile={}, list_photo_path=[], send_yes_no=True
    )

    sql = SQLighter("base/db.db")
    client = sql.get_client(user_id)

    # отправляем фото
    try:
        msg0 = await send_photo(chat_id, f"img/supp{random.randint(1,5)}.jpeg")
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

        await state.set_state(UserState.DESCRIPTION)

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
        await state.set_state(UserState.BEGINNING)


@dp.bot_started()
async def bot_started(event: BotStarted):
    await event.bot.send_message( # type: ignore
        chat_id=event.chat_id,
        text='Привет! Отправь мне /start'
    )