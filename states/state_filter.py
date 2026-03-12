from states.storage import storage


class StateFilter:

    def __init__(self, state):
        self.state = state

    async def __call__(self, event, data):

        chat_id = event.message.recipient.chat_id
        user_id = event.message.sender.user_id

        if chat_id is None:
            return False

        user = storage.get((chat_id, user_id))

        if not user:
            return False

        return user.get("state") == self.state
