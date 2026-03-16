import asyncio

from states.forms import Form
from loader import dp, bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_created(Form),
                    state=None,
                    content_types=types.ContentTypes.ANY)
async def bot_echo(message: types.Message):
    await message.delete()
    msg = await message.answer("""Начните заполнять заявку, нажимая на /start .
    Или отмените активную заявку на любой стадии, нажимая на /cancel""")
    await asyncio.sleep(10)
    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=msg.message_id)
    except MessageError as e:
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


