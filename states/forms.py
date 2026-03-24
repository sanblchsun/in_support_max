from maxapi.context import State, StatesGroup


class Form(StatesGroup):
    beginning = State()
    full_name = State()
    telefon = State()
    e_mail = State()
    firma = State()
    yes_no_save = State()
    description = State()
    priority = State()
    attach = State()
    attach_yes = State()
    send_request = State()