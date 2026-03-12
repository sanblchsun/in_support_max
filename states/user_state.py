# states/user_state.py
from enum import Enum


class UserState(Enum):
    BEGINNING = "beginning"
    FULL_NAME = "full_name"
    TELEFON = "telefon"
    EMAIL = "email"
    FIRMA = "firma"
    YES_NO_SAVE = "yes_no_save"
    INSERT_IN_BASE = "insert_in_base"
    DESCRIPTION = "description"
    PRIORITY = "priority"
    ATTACH = "attach"
    ATTACH_YES = "attach_yes"
    ATTACH_END = "attach_end"
    END_FORM = "end_form"
    SEND_REQUEST = "send_request"
    ADD_FOR_FIRM = "add_for_firm"
    UPDATE_FOR_FIRM = "update_for_firm"
    MESSAGE_FOR_EDIT = "message_for_edit"
    ERROR = "error"
    ID_SAVE = "id_save"
    WAITING = "waiting"


user_states: dict[int, "UserState"] = {}
