from base.sqlighter import SQLighter
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import Form
from aiogram.utils.exceptions import MessageError

@dp.message_handler(state=Form.states_names, commands=['cancel'])
@dp.message_handler(state=Form.states_names, text="Отказаться \U0001F644")
async def action_del_user_data(message: types.Message, state: FSMContext):
    end_reduest_message_id = await message.answer("Вы отменили заявку")
    data = await state.get_data()
    start_request_message_id = data.get("message_for_edit")
    for i in range(int(start_request_message_id), int(end_reduest_message_id)):
        try:
            await bot.delete_message(chat_id=message.from_user.id, message_id=i)
        except MessageError as e: ...
    await state.finish()



# функция для callback_query_handler, которые ниже
async def func_for_callback_query_handler(callback_query, state):
    end_reduest_message_id = await callback_query.message.answer("Вы отменили заявку")
    data = await state.get_data()
    start_request_message_id = data.get("message_for_edit")
    for i in range(int(start_request_message_id), int(end_reduest_message_id)):
        try:
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=i)
        except MessageError as e: ...
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "del_user_data", state=Form.states_names)
async def action_del_user_data(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    sql_object = SQLighter("base/db.db")
    sql_object.delete_user_data(callback_query.from_user.id)
    await func_for_callback_query_handler(callback_query, state)



@dp.callback_query_handler(lambda c: c.data in ["reject_request", "del_current_request"],
                           state=Form.states_names)
async def action_del_user_data(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    await func_for_callback_query_handler(callback_query, state)

@dp.callback_query_handler(lambda c: c.data == "send_no", state=Form.send_request)
async def action_request_to_support(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    await func_for_callback_query_handler(callback_query, state)
