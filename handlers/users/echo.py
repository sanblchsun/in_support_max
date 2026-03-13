# handlers/users/echo.py
import asyncio
from states.context import FSMContext
from states.user_state import UserState
from states.state_filter import StateFilter
from loader import dp, bot
from maxapi.filters import F
from maxapi.types import Attachment, Command, MessageCreated


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_created(StateFilter(state=UserState.BEGINNING))
async def bot_echo(event: MessageCreated, state: FSMContext):
    await event.message.delete()
    current_state = await state.get_state()
    msg = await event.message.answer(
        f"""Начните заполнять заявку, нажимая на /start .
    Или отмените активную заявку на любой стадии, нажимая на /cancel
    Ваша стадия: {current_state}"""
    )
    await asyncio.sleep(10)
    try:
        mid = msg.model_dump().get("message").get("body").get("mid")  # type: ignore
        await bot.delete_message(mid)
    except Exception as e:
        ...


# # Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
# @dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
#                     state=['Form:full_name', 'Form:telefon', 'Form:e_mail', 'Form:firma',
#                            'Form:beginning', 'Form:attach', 'Form:priority', 'Form:send_request'],
#                     content_types=types.ContentTypes.ANY)
# async def bot_echo_all(message: types.Message, state: FSMContext):
#     async def del_message(message, msg):
#         await asyncio.sleep(3)
#         try:
#             await bot.delete_message(chat_id=message.from_user.id, message_id=msg.message_id)
#         except MessageError as e:
#             ...

#     state_current = await state.get_state()
#     if state_current == 'Form:full_name':
#         await message.answer('Введите ваше Имя и Фамилию')
#     elif state_current == 'Form:telefon':
#         await message.answer('Введите ваш телефон')
#     elif state_current == 'Form:e_mail':
#         await message.answer('Введите ваш e-mail')
#     elif state_current == 'Form:firma':
#         await message.delete()
#         msg = await message.answer('Вы все еще на стадии заполнения заявки. \n\n'
#                              'Нажмите кнопку\n'
#                              'или \n'
#                              'для отмены заявки нажмите на ссылку /cancel')
#         await del_message(message, msg)
#     elif state_current == 'Form:beginning':
#         await message.delete()
#         msg = await message.answer('Вы все еще на стадии заполнения заявки. \n\n'
#                              'Нажмите кнопку\n'
#                              'или \n'
#                              'для отмены заявки нажмите на ссылку /cancel')
#         await del_message(message, msg)
