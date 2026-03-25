import asyncio
import re
import emoji
from loguru import logger
from maxapi import F
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated
from base.mysqlrequests import insert_request_to_mysql
from keyboards.inline.buttons import (
    attach_yes_no,
    buttons_priority,
    save_person_data,
    send_request_yes_no,
)
from mail.email_executor import send_email_in_executor
from utils.message_manager import add_message, delete_later, delete_messages
from loader import dp, bot
from states.forms import Form
from base.sqlighter import SQLighter
from .html import get_html


@dp.message_callback(F.callback.payload == "create_request", Form.beginning)
async def action_create_user_data(event: MessageCreated, context: MemoryContext):
    await delete_messages(context=context, bot=bot)
    msg = await event.message.answer("Укажите Ваши фамилию и имя:")
    await add_message(context=context, message=msg)
    await context.set_state(Form.full_name)


@dp.message_created(
    F.message.body.text, F.message.body.text.len() < 101, Form.full_name
)
async def action_full_name(event: MessageCreated, context: MemoryContext):
    await context.update_data(full_name=event.message.body.text)
    msg1 = await event.message.answer("Укажите Ваш контактный телефон:")
    await add_message(context=context, message=msg1)
    await context.set_state(Form.telefon)


@dp.message_created(F.message.body.text, F.message.body.text.len() < 101, Form.telefon)
async def action_telefon(event: MessageCreated, context: MemoryContext):
    await context.update_data(telefon=event.message.body.text)
    msg1 = await event.message.answer("Укажите Ваш e-mail:")
    await add_message(context=context, message=msg1)
    await context.set_state(Form.e_mail)


@dp.message_created(F.message.body.text, F.message.body.text.len() < 301, Form.e_mail)
async def action_e_mail(event: MessageCreated, context: MemoryContext):
    if not bool(
        re.search(
            r"^[\w\.\+\-]+\@[\w\.\-]+\.[a-z]{2,7}$",
            event.message.body.text,  # type: ignore
        )
    ):
        msg = await event.message.answer("Недействительный email ✉. Повторите")
        asyncio.create_task(delete_later(bot=bot, msg=msg, time_second=10))
        return

    await context.update_data(e_mail=event.message.body.text)
    msg1 = await event.message.answer("От какой компании обращаетесь:")
    await add_message(context=context, message=msg1)
    await context.set_state(Form.firma)


@dp.message_created(F.message.body.text, F.message.body.text.len() < 101, Form.firma)
async def action_insert_in_firma(event: MessageCreated, context: MemoryContext):
    await context.update_data(firma=event.message.body.text)
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
        await event.message.delete()
    except Exception as e:
        ...
    msg1 = await event.message.answer(
        """Отказ от сохранения.

Вы можете продолжать заполнять заявку.

Расскажите, что у вас случилось?"""
    )
    await add_message(context=context, message=msg1)
    await context.set_state(Form.description)


@dp.message_callback(F.callback.payload == "save_yes", Form.yes_no_save)
async def action_request_to_yes_save(event: MessageCreated, context: MemoryContext):
    await event.message.delete()
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


@dp.message_created(
    F.message.body.text, F.message.body.text.len() < 101, Form.description
)
async def action_description(event: MessageCreated, context: MemoryContext):
    await delete_messages(bot=bot, context=context)
    await context.update_data(description=event.message.body.text)
    html = get_html(description=event.message.body.text)  # type: ignore
    msg0 = await event.message.answer(html)
    await context.update_data(message_for_edit=msg0.message.body.mid)
    msg = await event.message.answer(
        "Укажите приоритет заявки:", attachments=[buttons_priority()]
    )
    await add_message(message=msg, context=context)
    await context.set_state(Form.priority)


async def next_priority(event: MessageCreated, context: MemoryContext):
    data = await context.get_data()
    html_request = get_html(description=data["description"], priority=data["priority"])
    try:
        await bot.edit_message(
            text=html_request,
            message_id=data["message_for_edit"],
        )
    except Exception as e:
        msg1 = await event.message.answer(html_request)
        await context.update_data(message_for_edit=msg1.message.body.mid)
    await delete_messages(bot, context)
    msg = await event.message.answer(
        emoji.emojize(":linked_paperclips:") + "Хотите приложить файлы и фотографии?",
        attachments=[attach_yes_no()],
    )
    await context.set_state(Form.attach)


@dp.message_callback(F.callback.payload == "low_btn_press", Form.priority)
async def action_low_btn_press(event: MessageCreated, context: MemoryContext):
    await context.update_data(priority="Низкий")
    await next_priority(event=event, context=context)


@dp.message_callback(F.callback.payload == "medium_btn_press", Form.priority)
async def action_medium_btn_press(event: MessageCreated, context: MemoryContext):
    await context.update_data(priority="Средний")
    await next_priority(event=event, context=context)


@dp.message_callback(F.callback.payload == "high_btn_press", Form.priority)
async def action_high_btn_press(event: MessageCreated, context: MemoryContext):
    await context.update_data(priority="Высокий")
    await next_priority(event=event, context=context)


@dp.message_callback(F.callback.payload == "critical_btn_press", Form.priority)
async def action_critical_btn_press(event: MessageCreated, context: MemoryContext):
    await context.update_data(priority="Критический")
    await next_priority(event=event, context=context)


@dp.message_callback(F.callback.payload == "attach_yes", Form.attach)
async def action_request_to_support1(event: MessageCreated, context: MemoryContext):
    try:
        await event.message.delete()
    except Exception as e:
        ...
    await event.message.answer(
        emoji.emojize(":linked_paperclips:") + "   вложите файл или сделайте фотографию"
    )
    await context.set_state(Form.attach_yes)


@dp.message_created(F.message.body.attachments, Form.attach_yes)
async def action_attach_yes(event: MessageCreated, context: MemoryContext):
    await delete_messages(bot=bot, context=context)
    current_state = await context.get_data()
    data_dist = current_state.get("dist_url_and_namefile")
    type_attach = event.message.body.attachments[0].type  # type: ignore
    if type_attach == "file":  # type: ignore
        doc_size = event.message.body.attachments[0].size  # type: ignore
        file_name = event.message.body.attachments[0].filename  # type: ignore
        if doc_size > 5120000:  # type: ignore
            msg = await event.message.reply(
                """В заявку вложен файл с недопустимым размером,
            повторите с файлом менее 5Мб """
            )
            await add_message(context=context, message=msg)
            return
    elif type_attach == "image":
        file_name0 = event.message.body.attachments[0].payload.photo_id  # type: ignore
        try:
            file_name = f"{str(file_name0)}.webp"
        except Exception as e:
            file_name = "file"
    elif type_attach == "video":
        msg1 = await event.message.answer(
            """Пока нельзя вкладывать видео файлы,
нажимая 'Фото или видео'.
Вставляйте видео файлы как 'Файл'."""
        )
        await delete_later(msg=msg1, bot=bot, time_second=10)
        msg2 = await event.message.answer(
            "Можете вложить еще файлы или отправить заявку.",
            attachments=[send_request_yes_no()],
        )
        await add_message(context=context, message=msg2)
        return
    else:
        file_name = "file"

    url_file = event.message.body.attachments[0].payload.url  # type: ignore
    data_dist[file_name] = url_file  # type: ignore
    await context.update_data(dist_url_and_namefile=data_dist)
    msg = await event.message.answer(
        "Можете вложить еще файлы или отправить заявку.",
        attachments=[send_request_yes_no()],
    )
    await add_message(context=context, message=msg)


@dp.message_callback(F.callback.payload == "send_yes", Form.attach_yes)
async def action_attach_send_request(event: MessageCreated, context: MemoryContext):
    await context.set_state(Form.send_request)


@dp.message_callback(F.callback.payload == "attach_no", Form.attach)
async def action_attach(event: MessageCreated, context: MemoryContext):
    try:
        await event.message.delete()
    except Exception as e:
        ...
    msg = await event.message.answer(
        emoji.emojize(":envelope: отправить заявку?"),
        attachments=[send_request_yes_no()],
    )
    await add_message(context=context, message=msg)
    await context.set_state(Form.send_request)


@dp.message_callback(F.callback.payload == "send_yes", Form.send_request)
async def action_request_to_support(event: MessageCreated, context: MemoryContext):

    user_id = event.from_user.user_id
    corrent_state = await context.get_data()

    await insert_request_to_mysql(
        e_mail=corrent_state["e_mail"],
        firma=corrent_state["firma"],
        full_name=corrent_state["full_name"],
        cont_telefon=corrent_state["telefon"],
        description=corrent_state["description"],
        priority=corrent_state["priority"],
        message_id=user_id,
    )
    msg0 = await event.message.answer("📨 Начинаю отправку заявки.")
    await add_message(context=context, message=msg0)

    # отправляем email через executor (не блокирует event loop)
    ident_error = await send_email_in_executor(
        full_name=corrent_state["full_name"],
        e_mail=corrent_state["e_mail"],
        firma=corrent_state["firma"],
        cont_telefon=corrent_state["telefon"],
        description=corrent_state["description"],
        priority=corrent_state["priority"],
        user_id=user_id,
        http_to_attach=corrent_state["dist_url_and_namefile"],
    )

    if ident_error:
        await event.message.answer(
            f"Ошибка при отправке заявки: {ident_error}. "
            f"Что то пошло не так, обратитесь к поставщику продукта"
        )
        await delete_messages(bot=bot, context=context)
    else:
        await event.message.answer(
            f"""Заявка отправлена. Номер зарегистрированной заявки придет на контактную почту.
Чтобы направить еще одну заявку, нажмите /start"""
        )
        await delete_messages(bot=bot, context=context)
    await context.clear()
