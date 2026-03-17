from maxapi.context import State, StatesGroup


class Form(StatesGroup):
    beginning = State()
    full_name = State()
    telefon = State()
    e_mail = State()
    firma = State()
    yes_no_save = State()
    insert_in_base = State()
    description = State()
    priority = State()
    attach = State()
    attach_yes = State()
    attach_end = State()
    end_form = State()
    send_request = State()
    add_for_firm = State()
    update_for_firm = State()
    message_for_edit = State()
    error = State()
    id_save = State()
    waiting = State()