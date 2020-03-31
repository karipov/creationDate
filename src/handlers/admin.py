"""
This file is for administrative commands only.
"""
import json, pathlib  # noqa: E401
from aiogram import types

ADMINS = json.load(open(pathlib.Path.cwd().joinpath('config.json')))['ADMINS']


async def stats(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer("You're an admin!")
    else:
        pass
