from aiogram.utils.exceptions import MessageError

from loader import dp, bot
from states.state_form import Form
from aiogram import types
from aiogram.dispatcher import FSMContext
# from keyboards.inline.buttons import *
from keyboards.default.buttons import *


@dp.message_handler(state=Form.attach_yes, content_types=['text'])
async def message_error(message: types.Message, state: FSMContext):
    await message.delete()
    try:
        await bot.edit_message_text("""Сейчас нужно вложить файл или сделать фото
            или отмените заявку, нажав /cancel
            """, chat_id=message.from_user.id, message_id=message.message_id - 1)
    except MessageError as e:
        ...


@dp.message_handler(state=Form.attach_yes, content_types=['video'])
async def action_document(message: types.Message, state: FSMContext):
    doc_size = message.video.file_size
    if doc_size > 18874368:
        await message.reply("""В заявку вложен файл с недопустимым размером,
        повторите с файлом менее 20Мб """)
        await message.delete()
        return
    keyboard = send_request_yes_no_def()
    await message.reply(f'В заявку вложен файл: {message.video.file_name}', reply_markup=keyboard)
    url_file = await message.video.get_url()
    async with state.proxy() as data:
        data['dist_url_and_namefile'][url_file] = (message.from_user.id, message.message_id, message.video.file_name)
    await state.set_state(Form.send_request)


@dp.message_handler(state=Form.attach_yes, content_types=['document'])
async def action_document(message: types.Message, state: FSMContext):
    doc_size = message.document.file_size
    if doc_size > 18874368:
        await message.reply("""В заявку вложен файл с недопустимым размером,
        повторите с файлом менее 20Мб """)
        await message.delete()
        return
    keyboard = send_request_yes_no_def()
    await message.reply(f'В заявку вложен файл: {message.document.file_name}', reply_markup=keyboard)
    url_file = await message.document.get_url()
    async with state.proxy() as data:
        data['dist_url_and_namefile'][url_file] = (message.from_user.id, message.message_id, message.document.file_name)
    await state.set_state(Form.send_request)


@dp.message_handler(state=Form.attach_yes, content_types=['photo'])
async def action_photo(message: types.Message, state: FSMContext):
    doc_size = message.photo[-1].file_size
    if doc_size > 18874368:
        await message.reply("""В заявку вложен файл с недопустимым размером,
        повторите с файлом менее 20Мб """)
        await message.delete()
        return
    keyboard = send_request_yes_no_def()
    await message.reply('В заявку вложено фото: ', reply_markup=keyboard)
    url_file = await message.photo[-1].get_url()
    file_name = str(url_file).split('/')[-1]
    async with state.proxy() as data:
        data['dist_url_and_namefile'][url_file] = (message.from_user.id, message.message_id, file_name)
    await state.set_state(Form.send_request)
