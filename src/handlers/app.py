"""
Reserved for commands that pertain to the main functionality of the bot
"""
import pathlib, json  # noqa: E401
import logging

from aiogram import types
from telethon.tl.types import InputPeerUser
from telethon.errors import FloodWaitError

from process.database import User
from process.function import Function
from process.utility import (
    clean_message, tree_display, escape_dict, time_format
)


REPLIES = json.load(open(pathlib.Path.cwd().joinpath('src/ui/replies.json')))
interpolation = Function()
logger = logging.getLogger(__name__)


async def reply_with_age(message: types.Message):
    user, _ = User.get_or_create(
        user_id=message.from_user.id,
        defaults={'language': 'en'}
    )

    if message.forward_sender_name:
        await message.answer(
            text=REPLIES['forward_link'][user.language]
        )
        return

    clean = clean_message(message)

    for key, value in clean.items():
        if not (key == 'forward_from' or key == 'from'):
            continue

        # interpolate the date
        date = time_format(
            unix_time=interpolation.func(int(value['id']))
        )
        clean[key]['registered'] = date

        logger.info(
            f"{user.user_id} requested date for ID {int(value['id'])}, "
            f"received date {date}"
        )

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
        entity = await self.client.get_input_entity(username)
    except ValueError:
        await message.answer(
            text=REPLIES['no_username'][user.language]
        )
        return
    except FloodWaitError as e:
        sec = e.seconds
        if sec > 60:
            time_left = f"{sec // 60}m {sec % 60}s"
        else:
            time_left = f"{sec}s"

        await message.answer(
            text=REPLIES['many_requests'][user.language].format(time_left)
        )
        return

    if not isinstance(entity, InputPeerUser):
        await message.answer(
            text=REPLIES['no_username'][user.language]
        )
        return

    data = await self.client.get_entity(entity)
    data = data.to_dict()

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

    logger.info(
        f"{user.user_id} requested username {username} with id {user_id}"
        f""
    )

    await message.answer(
        text=tree,
        parse_mode='HTML'
    )

    user.requests += 1
    user.save()
