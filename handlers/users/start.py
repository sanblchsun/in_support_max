import asyncio
import logging
import random
from base.sqlighter import SQLighter
from loader import dp, bot
from states.context import FSMContext
from states.get_state import get_state
from states.user_state import UserState
from keyboards.inline.buttons import request_delete_with_data, request_or_reject
from .message_del import msg_delete
from maxapi.types import Command, MessageCreated
import redis.asyncio as redis


@dp.message_created(Command("start"))
async def bot_start(event: MessageCreated, state: FSMContext):
    await state.set(UserState.WAITING)
    await event.message.answer(
        "Начат процесс подачи заявки. Если он не будет завершён за 30 минут, "
        "то произойдет  автоматическая отмена Вашей заявки."
    )

    # Запускаем задачу сброса состояния через 30 минут
    asyncio.create_task(
        reset_state_after_timeout(
            state,
            message.chat.id,
            message.from_user.full_name,
            message.from_user.id,
            30 * 60,
        )
    )  # 30 минут

    async with state.proxy() as data:
        data["dist_url_and_namefile"] = {}
        data["list_photo_path"] = []
        data["send_yes_no"] = True

    sql_object = SQLighter("base/db.db")
    list_data_client = sql_object.get_client(message.from_user.id)
    if bool(len(list_data_client)):
        keyboard = request_delete_with_data()
        try:
            i = random.randint(1, 5)
            await message.answer_photo(
                photo=InputFile(f"img/supp{i}.jpeg"), reply_markup=ReplyKeyboardRemove()
            )
        except FileNotFoundError as e:
            pass
        msg = await message.answer(
            f"Привет, {message.from_user.full_name}!\n\n"
            f"Ваши данные для автозаполнения формы заявки:\n\n"
            f"ФИО: {list_data_client[0][1]}\n"
            f"Организация: {list_data_client[0][2]}\n"
            f"e-mail: {list_data_client[0][3]}\n"
            f"телефон: {list_data_client[0][4]}",
            reply_markup=keyboard,
        )
        await state.update_data(message_for_edit=msg.message_id)
        await event.message.answer("Расскажите - что у вас случилось?")
        await state.set_state(Form.description)
        await state.update_data(full_name=list_data_client[0][1])
        await state.update_data(firma=list_data_client[0][2])
        await state.update_data(e_mail=list_data_client[0][3])
        await state.update_data(telefon=list_data_client[0][4])
        await message.delete()
    else:
        try:
            i = random.randint(1, 5)
            msg = await message.answer_photo(
                photo=InputFile(f"img/supp{i}.jpeg"), reply_markup=ReplyKeyboardRemove()
            )
        except FileNotFoundError as e:
            pass
        keyboard = request_or_reject()
        await event.message.answer(
            """Уважаемый пользователь, вас приветствует ТГ-бот ИИС!
Прошу Вас ответить на несколько вопросов,
которые мне необходимо задать для отправки
Вашей заявки в техническую поддержку.""",
            reply_markup=keyboard,
        )
        await state.set_state(Form.beginning)
        await state.update_data(message_for_edit=msg.message_id)


async def reset_state_after_timeout(
    state: FSMContext, chat_id, user_name, user_id, delay: int
):
    await asyncio.sleep(delay)
    # Проверяем текущее состояние перед сбросом
    current_state = await state.get_state()
    if current_state is not None:  # если состояние ещё активно
        msg = await bot.send_message(
            chat_id,
            f"⏰⏰⏰ Ваша заявка отменена в связи с истечением времени на её подачу. "
            "Пожалуйста, нажмите /start.",
        )
        logging.info(
            f"""Ваша заявка отменена в связи с истечением времени на её подачу. 
{current_state} {user_name} {user_id}"""
        )
        data = await state.get_data()
        msg_start = data.get("message_for_edit")
        await msg_delete(msg_start, msg.message_id, chat_id)
        await state.finish()
