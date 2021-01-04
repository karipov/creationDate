"""
Service messages for commands such as /help and /start
"""
import json, pathlib  # noqa: E401
import logging

from aiogram import types

from process.database import User
from . import app


REPLIES = json.load(open(pathlib.Path.cwd().joinpath("src/ui/replies.json")))
LANG_KEY = types.InlineKeyboardMarkup(row_width=3)
LANG_KEY.add(
    *(
        types.InlineKeyboardButton(t, callback_data=d)
        for t, d in zip(REPLIES["LANGS_NAMES"], REPLIES["LANGS"])
    )
)
logger = logging.getLogger(__name__)


async def start(message: types.Message):
    """
    Handler for /start commands
    """
    user, _ = User.get_or_create(user_id=message.from_user.id)

    logger.info(f"{user.user_id} entered /start")

    if user.language == "none":
        # auto-logs a user's language from telegram-given data
        if getattr(message.from_user, "language_code", None) in REPLIES["LANGS"]:
            user.language = message.from_user.language_code
        else:
            user.language = "en"  # default language

        user.save()

        await message.answer(
            text=REPLIES["lang"]["en"], reply_markup=LANG_KEY, parse_mode="HTML"
        )

    await message.answer(REPLIES["start"][user.language], parse_mode="HTML")
    await app.reply_with_age(message)

    user.requests += 1
    user.save()


async def lang(message: types.Message):
    user, _ = User.get_or_create(
        user_id=message.from_user.id, defaults={"language": "en"}
    )

    await message.answer(
        text=REPLIES["lang"][user.language], reply_markup=LANG_KEY, parse_mode="HTML"
    )

    logger.info(f"{user.user_id} entered /lang")

    user.requests += 1
    user.save()


async def help(message: types.Message):
    user, _ = User.get_or_create(
        user_id=message.from_user.id, defaults={"language": "en"}
    )

    await message.answer(text=REPLIES["help"][user.language], parse_mode="HTML")

    logger.info(f"{user.user_id} entered /help")

    user.requests += 1
    user.save()


async def credits(message: types.Message):
    user, _ = User.get_or_create(
        user_id=message.from_user.id, defaults={"language": "en"}
    )

    await message.answer(text=REPLIES["credits"][user.language], parse_mode="HTML")

    logger.info(f"{user.user_id} entered /credits")

    user.requests += 1
    user.save()
