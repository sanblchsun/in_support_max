from states.context import storage


class StateFilter:

    def __init__(self, state):
        self.state = state

    async def __call__(self, event, data):

        user_id = event.message.sender.user_id

        user = storage.get(user_id)

        if not user:
            return False

        return user.get("state") == self.state
