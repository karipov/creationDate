"""
Service messages for commands such as /help and /start
"""
import json, pathlib  # noqa: E401
from aiogram import types

replies = json.load(open(pathlib.Path.cwd().joinpath('src/ui/replies.json')))


async def start(message: types.Message):
    message.answer()
