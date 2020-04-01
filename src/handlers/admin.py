"""
This file is for administrative commands only.
"""
from pathlib import Path
from aiogram import types
from process.database import User


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
        with open(Path.cwd().joinpath('src/data/users.db')) as file:
            await message.answer_document(file)

    elif payload == ['lang']:
        text = 'Language Percentages:'
        distinct_langs = (
            User
            .select(User.language)
            .distinct()
            .scalar(as_tuple=True)
        )

        for lang in distinct_langs:
            total_users = User.select().where(
                User.is_ban == False
            ).count()  # noqa: E712
            total_lang = User.select().where(User.language == lang).count()
            percent = round(total_lang / total_users * 100, 2)
            text += f'\n{lang}: {percent}'

        await message.answer(text)

    else:
        await message.answer(subcommands)
