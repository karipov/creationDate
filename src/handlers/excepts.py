import pathlib, json  # noqa: E401
import logging

from aiogram import Bot, types

CONFIG = json.load(open(pathlib.Path.cwd().joinpath("src/config.json")))
logger = logging.getLogger(__name__)


async def on_err(event: types.Update, exception: Exception):
    bot = Bot.get_current()

    # notifies the admins
    for admin in CONFIG["ADMINS"]:
        await bot.send_message(admin, f"{exception} ocurred on event: {event}")

    # logs the error in the logger
    logger.critical(f"<{exception}> ocurred on event: {event}")

    return True
