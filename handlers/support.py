from maxapi import F
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated
from utils.message_manager import add_message
from loader import dp
from states.forms import Form


@dp.message_callback(F.callback.payload == "create_request", Form.beginning)
async def action_create_user_data(event: MessageCreated, context: MemoryContext):
    msg = await event.message.answer("Укажите Ваши фамилию и имя:")
    await add_message(context=context, message=msg)
    await context.set_state(Form.full_name)
    

@dp.message_created(F.message.body.text, Form.full_name)
async def action_full_name(event: MessageCreated, context: MemoryContext):
    if len(event.model_dump().get("message").get("body").get("text")) > 100:
        msg = await event.message.answer("""Разрешено не больше 100 знаков.
        Введите пожалуйста Ваши фамилию и имя:""")
        await add_message(context=context, message=msg)
        return
    await context.update_data(full_name=event.model_dump().get("message").get("body").get("text"))
    msg1 = await event.message.answer("Укажите Ваш контактный телефон:")
    await add_message(context=context, message=msg1)
    await context.set_state(Form.telefon)