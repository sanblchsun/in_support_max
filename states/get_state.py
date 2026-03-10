from states.context import FSMContext


def get_state(event):
    user_id = event.message.sender.user_id
    return FSMContext(user_id)
