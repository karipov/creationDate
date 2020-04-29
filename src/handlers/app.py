"""
Reserved for commands that pertain to the main functionality of the bot
"""
import pathlib, json  # noqa: E401

from aiogram import types
from telethon.tl.types import User as TelethonUser

from process.database import User
from process.function import Function
from process.utility import (
    clean_message, tree_display, escape_dict, time_format
)

import logging

REPLIES = json.load(open(pathlib.Path.cwd().joinpath('src/ui/replies.json')))
interpolation = Function()


async def reply_with_age(message: types.Message):
    user, _ = User.get_or_create(
        user_id=message.from_user.id,
        defaults={'language': 'en'}
    )
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


# Middleware function
# dynamically added to a class; uses self to access the Telethon client.
async def username_reply(self, message: types.Message):
    user, _ = User.get_or_create(
        user_id=message.from_user.id,
        defaults={'language': 'en'}
    )

    username = message.entities[0].get_text(message.text)
    # telethon automatically sleeps on FloodError

    try:
        data = await self.client.get_entity(username)
    except ValueError:
        await message.answer(
            text=REPLIES['no_username'][user.language]
        )
        return

    if not isinstance(data, TelethonUser):
        await message.answer(
            text=REPLIES['no_username'][user.language]
        )
        return

    data = data.to_dict()

    logging.info(data['id'])

    # dictionary cleaning
    for key in list(data.keys()):
        if key not in [
            'first_name', 'last_name', 'id', 'username'
        ] or not data[key]:
            del data[key]

    user_id = data['id']
    data['registered'] = time_format(
        unix_time=interpolation.func(user_id)
    )
    escaped = escape_dict(data)

    # formatting
    tree = REPLIES['user'][user.language]
    tree += tree_display(escaped)

    await message.answer(
        text=tree,
        parse_mode='HTML'
    )

    user.requests += 1
    user.save()
