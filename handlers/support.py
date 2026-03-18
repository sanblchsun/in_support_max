import asyncio
import re
import emoji
from maxapi import F
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated
from keyboards.inline.buttons import save_person_data
from utils.message_manager import add_message, delete_later
from loader import dp, bot
from states.forms import Form
from base.sqlighter import SQLighter
from .html import get_html


@dp.message_callback(F.callback.payload == "create_request", Form.beginning)
async def action_create_user_data(event: MessageCreated, context: MemoryContext):
    msg = await event.message.answer("Укажите Ваши фамилию и имя:")
    await add_message(context=context, message=msg)
    await context.set_state(Form.full_name)


@dp.message_created(F.message.body.text.len() < 101, Form.full_name)
async def action_full_name(event: MessageCreated, context: MemoryContext):
    await context.update_data(
        full_name=event.model_dump().get("message").get("body").get("text")
    )
    msg1 = await event.message.answer("Укажите Ваш контактный телефон:")
    await add_message(context=context, message=msg1)
    await context.set_state(Form.telefon)


@dp.message_created(F.message.body.text.len() < 101, Form.telefon)
async def action_telefon(event: MessageCreated, context: MemoryContext):
    await context.update_data(
        telefon=event.model_dump().get("message").get("body").get("text")
    )
    msg1 = await event.message.answer("Укажите Ваш e-mail:")
    await add_message(context=context, message=msg1)
    await context.set_state(Form.e_mail)


@dp.message_created(F.message.body.text.len() < 101, Form.e_mail)
async def action_e_mail(event: MessageCreated, context: MemoryContext):
    if not bool(
        re.search(
            r"^[\w\.\+\-]+\@[\w\.\-]+\.[a-z]{2,7}$",
            event.model_dump().get("message").get("body").get("text"),
        )
    ):
        msg = await event.message.answer("Недействительный email ✉. Повторите")
        asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=10))
        return

    await context.update_data(
        e_mail=event.model_dump().get("message").get("body").get("text")
    )
    msg1 = await event.message.answer("От какой компании обращаетесь:")
    await add_message(context=context, message=msg1)
    await context.set_state(Form.firma)


@dp.message_created(F.message.body.text.len() < 101, Form.firma)
async def action_insert_in_firma(event: MessageCreated, context: MemoryContext):
    await context.update_data(
        firma=event.model_dump().get("message").get("body").get("text")
    )
    msg1 = await event.message.answer(
        """Я могу сохранить Ваши данные,
чтобы в следующий раз их не нужно было вводить при
отправке заявки.
Нажимая кнопку «ДА», Вы даете согласие на обработку Ваших персональных данных.""",
        attachments=[save_person_data()],
    )
    await add_message(context=context, message=msg1)
    await context.set_state(Form.yes_no_save)


@dp.message_callback(F.callback.payload == "save_no", Form.yes_no_save)
async def action_request_to_no_save(event: MessageCreated, context: MemoryContext):
    try:
        msg1 = await event.message.edit(
            emoji.emojize(
                """Отказ от сохранения.

Вы можете продолжать заполнять заявку.

Расскажите, что у вас случилось?"""
            )
        )
        await add_message(context=context, message=msg1)
    except Exception as e:
        ...
    await context.set_state(Form.description)


@dp.message_callback(F.callback.payload == "save_yes", Form.yes_no_save)
async def action_request_to_yes_save(event: MessageCreated, context: MemoryContext):
    sql_object = SQLighter("base/db.db")
    current_state = await context.get_data()
    user_id = event.from_user.user_id
    sql_object.add_user(
        user_id,
        current_state["full_name"],
        current_state["telefon"],
        current_state["e_mail"],
        current_state["firma"],
    )
    msg1 = await event.message.answer(
        """Спасибо, Ваши данные сохранены и будут автоматически использоваться при подаче всех последующих заявок.

Вы можете продолжать заполнять заявку.

Расскажите, что у вас случилось?"""
    )
    await add_message(context=context, message=msg1)
    await context.set_state(Form.description)


@dp.message_created(F.message.body.text, Form.description)
async def action_description(event: MessageCreated, context: MemoryContext):
    html = get_html(
        description=event.model_dump().get("message").get("body").get("text")
    )
    data = await context.get_data()
    try:
        await bot.edit_message(
            text=html,
            message_id=data["message_for_edit"].model_dump().get("message").get("body").get("text"),
        )
    except Exception as e: ...
