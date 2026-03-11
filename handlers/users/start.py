import random
from base.sqlighter import SQLighter
from loader import dp, bot
from states.context import FSMContext
from states.user_state import UserState
from keyboards.inline.buttons import request_delete_with_data
from maxapi.types import Command, InputMedia, Attachment, MessageCreated


# ---- helper для отправки фото ----
async def send_photo(chat_id: int, photo_path: str, text: str | None = None):
    return await bot.send_message(
        chat_id=chat_id,
        attachments=[InputMedia(type="photo", media=photo_path)],  # type: ignore
        text=text,
    )


@dp.message_created(Command("start"))
async def bot_start(event: MessageCreated, state: FSMContext):

    await state.set_state(UserState.WAITING)

    await event.message.answer(
        "Начат процесс подачи заявки. Если он не будет завершён за 30 минут, "
        "то произойдет  автоматическая отмена Вашей заявки."
    )

    # Запускаем задачу сброса состояния через 30 минут
    await state.set_timeout(1800)

    await state.update_data(
        dist_url_and_namefile={}, list_photo_path=[], send_yes_no=True
    )

    sql_object = SQLighter("base/db.db")
    list_data_client = sql_object.get_client(event.from_user.user_id)  # type: ignore
    chat_id = event.message.recipient.chat_id

    i = random.randint(1, 5)
    if bool(len(list_data_client)):
        try:
            if chat_id is None:
                return
            await send_photo(chat_id, f"img/supp{i}.jpeg")
        except FileNotFoundError as e:
            pass
        msg = await event.message.answer(
            f"Привет, {event.from_user.full_name}!\n\n"  # type: ignore
            f"Ваши данные для автозаполнения формы заявки:\n\n"
            f"ФИО: {list_data_client[0][1]}\n"
            f"Организация: {list_data_client[0][2]}\n"
            f"e-mail: {list_data_client[0][3]}\n"
            f"телефон: {list_data_client[0][4]}",
            attachments=[request_delete_with_data()],
        )
        await state.add_message(msg)

        await event.message.answer("Расскажите - что у вас случилось?")
        await state.set_state(UserState.DESCRIPTION)
        await state.update_data(full_name=list_data_client[0][1])
        await state.update_data(firma=list_data_client[0][2])
        await state.update_data(e_mail=list_data_client[0][3])
        await state.update_data(telefon=list_data_client[0][4])
        await event.message.delete()
    else:
        try:
            if chat_id is None:
                return
            await send_photo(chat_id, f"img/supp{i}.jpeg")
        except FileNotFoundError:
            pass
        await event.message.answer(
            """Уважаемый пользователь, вас приветствует ТГ-бот ИИС!
Прошу Вас ответить на несколько вопросов,
которые мне необходимо задать для отправки
Вашей заявки в техническую поддержку.""",
            attachments=[request_delete_with_data()],
        )
        await state.set_state(UserState.BEGINNING)
