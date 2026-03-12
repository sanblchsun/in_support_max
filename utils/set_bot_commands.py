from maxapi.types import BotCommand


async def set_default_commands(bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(name="start", description="Создать заявку"),
            BotCommand(name="cancel", description="Отменить заявку"),
        ]
    )
