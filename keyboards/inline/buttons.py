from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def request_delete_with_data():
    del_btn = InlineKeyboardButton("отменить заявку и стереть свои данные", callback_data="del_user_data")
    del_btn1 = InlineKeyboardButton("Отмена заявки", callback_data="reject_request")
    return InlineKeyboardMarkup().add(del_btn).add(del_btn1)


def attach_yes_no():
    no_btn = InlineKeyboardButton("НЕТ", callback_data="attach_no")
    yes_btn = InlineKeyboardButton("ДА", callback_data="attach_yes")
    return InlineKeyboardMarkup().add(no_btn, yes_btn)


def send_request_yes_no():
    no_btn = InlineKeyboardButton("НЕТ", callback_data="send_no")
    yes_btn = InlineKeyboardButton(" ДА", callback_data="send_yes")
    return InlineKeyboardMarkup().add(no_btn, yes_btn)


def request_or_reject():
    rqsr_btn = InlineKeyboardButton('Согласиться', callback_data='create_request')
    del_btn = InlineKeyboardButton("Отказаться", callback_data="del_current_request")
    return InlineKeyboardMarkup().add(rqsr_btn, del_btn)


def reject_request():
    del_btn = InlineKeyboardButton("Отмена заявки", callback_data="reject_request")
    return InlineKeyboardMarkup().add(del_btn)

def save_person_data():
    no_btn = InlineKeyboardButton("НЕТ", callback_data="save_no")
    yes_btn = InlineKeyboardButton("ДА", callback_data="save_yes")
    return InlineKeyboardMarkup().add(yes_btn, no_btn)


def buttons_priority():
    low_btn = InlineKeyboardButton("Низкий", callback_data="low_btn_press")
    medium_btn = InlineKeyboardButton("средний", callback_data="medium_btn_press")
    high_btn = InlineKeyboardButton("высокий", callback_data="high_btn_press")
    critical_btn = InlineKeyboardButton("критический", callback_data="critical_btn_press")
    return InlineKeyboardMarkup().add(low_btn).\
        add(medium_btn).\
        add(high_btn).\
        add(critical_btn)

def btn_get_status():
    btn = InlineKeyboardButton("Узнайте статус заявки", callback_data='btn_get_status')
    return InlineKeyboardMarkup().add(btn)