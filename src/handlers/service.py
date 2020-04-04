"""
Service messages for commands such as /help and /start
"""
import json, pathlib  # noqa: E401
from aiogram import types
from process.database import User


REPLIES = json.load(open(pathlib.Path.cwd().joinpath('src/ui/replies.json')))
LANG_KEY = types.InlineKeyboardMarkup(row_width=3)
LANG_KEY.add(
    *(types.InlineKeyboardButton(t, callback_data=d) for t, d in zip(
        REPLIES['LANGS_NAMES'], REPLIES['LANGS']
    ))
)


async def start(message: types.Message):
    """
    Handler for /start commands
    """
    user, _ = User.get_or_create(user_id=message.from_user.id)

    if not user.language == 'none':
        await message.answer(REPLIES['start'][user.language])

        user.requests += 1
        user.save()
        return

    await message.answer(
        text=REPLIES['lang']['en'],
        reply_markup=LANG_KEY,
        parse_mode='HTML'
    )

    # auto-logs a user's language from telegram-given data
    if getattr(message.from_user, 'language_code', None) in REPLIES['LANGS']:
        user.language = message.from_user.language_code
    else:
        user.language = 'en'  # default language

    user.requests += 1
    user.save()


async def lang(message: types.Message):
    user = User.get(User.user_id == message.from_user.id)

    await message.answer(
        text=REPLIES['lang'][user.language],
        reply_markup=LANG_KEY,
        parse_mode='HTML'
    )

    user.requests += 1
    user.save()


async def help(message: types.Message):
    user = User.get(User.user_id == message.from_user.id)

    await message.answer(
        text=REPLIES['help'][user.language],
        parse_mode='HTML'
    )

    user.requests += 1
    user.save()


async def credits(message: types.Message):
    user = User.get(User.user_id == message.from_user.id)

    await message.answer(
        text=REPLIES['credits'][user.language],
        parse_mode='HTML'
    )

    user.requests += 1
    user.save()
