"""
Reserved for commands that pertain to the main functionality of the bot
"""
import pathlib, json  # noqa: E401
from aiogram import types
from process.database import User
from process.function import Function
from process.utility import (
    clean_message, tree_display, escape_dict, time_format
)

REPLIES = json.load(open(pathlib.Path.cwd().joinpath('src/ui/replies.json')))
interpolation = Function()


async def reply_with_age(message: types.Message):
    user = User.get(User.user_id == message.from_user.id)
    clean = clean_message(message)

    for key, value in clean.items():
        if not (key == 'forward_from' or key == 'from'):
            continue

        # interpolate the date
        date = time_format(
            unix_time=interpolation.func(int(value['id']))
        )
        clean[key]['registered'] = date

    escaped = escape_dict(clean)

    tree = REPLIES['message'][user.language]
    tree += tree_display(escaped)

    await message.answer(
        text=tree,
        parse_mode='HTML'
    )

    user.requests += 1
    user.save()
