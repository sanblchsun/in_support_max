# keyboards/inline/buttons.py
from maxapi.types import (
    LinkButton,
    MessageButton,
    MessageCreated,
    BotStarted,
    MessageCallback,
    Command,
    CallbackButton,
    ButtonsPayload,
    Attachment,
    BotCommand,
)
from maxapi.enums.intent import Intent
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder


def request_delete_with_data() -> Attachment:
    buttons = InlineKeyboardBuilder()
    buttons.row(
        CallbackButton(
            text="отменить заявку и стереть свои данные",
            payload="del_user_data",
        )
    )
    buttons.row(
        CallbackButton(
            text="Отмена заявки",
            payload="reject_request",
        )
    )

    return buttons.as_markup()


def attach_yes_no():
    buttons = InlineKeyboardBuilder()
    buttons.row(
        CallbackButton(
            text="НЕТ",
            payload="attach_no",
        ),
        CallbackButton(
            text="ДА",
            payload="attach_yes",
        ),
    )
    return buttons.as_markup()


def request_or_reject() -> Attachment:
    buttons = InlineKeyboardBuilder()
    buttons.row(
        CallbackButton(
            text="Согласиться",
            payload="create_request",
        ),
        CallbackButton(
            text="Отказаться",
            payload="del_current_request",
        ),
    )
    return buttons.as_markup()


def reject_request():
    buttons = InlineKeyboardBuilder()
    buttons.row(
        CallbackButton(
            text="Отмена заявки",
            payload="reject_request",
        ),
    )
    return buttons.as_markup()


def save_person_data():
    buttons = InlineKeyboardBuilder()
    buttons.row(
        CallbackButton(
            text="НЕТ",
            payload="save_no",
        ),
        CallbackButton(
            text="ДА",
            payload="save_yes",
        ),
    )
    return buttons.as_markup()


def buttons_priority():
    buttons = InlineKeyboardBuilder()
    buttons.row(
        CallbackButton(
            text="Низкий",
            payload="low_btn_press",
        )
    )
    buttons.row(
        CallbackButton(
            text="средний",
            payload="medium_btn_press",
        )
    )
    buttons.row(
        CallbackButton(
            text="высокий",
            payload="high_btn_press",
        )
    )
    buttons.row(
        CallbackButton(
            text="критический",
            payload="critical_btn_press",
        ),
    )
    return buttons.as_markup()


def send_request_yes_no():
    buttons = InlineKeyboardBuilder()
    buttons.row(
        CallbackButton(
            text="отказаться",
            payload="send_no",
        )
    )
    buttons.row(
        CallbackButton(
            text="отправить заявку",
            payload="send_yes",
        ),
    )
    return buttons.as_markup()


def start():
    buttons = InlineKeyboardBuilder()
    buttons.row(MessageButton(text="/start"))
    return buttons.as_markup()