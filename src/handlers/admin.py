"""
This file is for administrative commands only.
"""
from pathlib import Path
import json
import logging

from aiogram import types
from process.database import User


REPLIES = json.load(open(Path.cwd().joinpath('src/ui/replies.json')))
logger = logging.getLogger(__name__)


async def stats(message: types.Message):
    payload = message.get_args().split()
    subcommands = [
        ['total'],
        ['file'],
        ['lang']
    ]

    if payload == ['total']:
        total_users = User.select().where(
            User.is_ban == False
        ).count()  # noqa: E712
        await message.answer(total_users)

    elif payload == ['file']:
        file = open(Path.cwd().joinpath('src/data/users.db'), 'rb')
        input_file = types.InputFile(file)

        await message.answer_document(input_file)

        file.close()

    elif payload == ['lang']:
        text = 'Language Percentages:'
        top_list = []

        for lang in REPLIES['LANGS']:
            total_users = User.select().where(
                User.is_ban == False
            ).count()  # noqa: E712
            total_lang = User.select().where(User.language == lang).count()

            try:
                percent = total_lang / total_users
            except ZeroDivisionError:
                percent = 0.0

            top_list.append([lang, percent])

        for lang, per in sorted(top_list, key=lambda x: x[1], reverse=True):
            text += f'\n<pre>{lang}: {per:.2%}</pre>'

        await message.answer(
            text=text,
            parse_mode='HTML'
        )

    else:
        await message.answer(subcommands)
