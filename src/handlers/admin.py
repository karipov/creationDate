"""
This file is for administrative commands only.
"""
from pathlib import Path
import json
import logging

from aiogram import types
from peewee import fn
from process.database import User


REPLIES = json.load(open(Path.cwd().joinpath("src/ui/replies.json")))
logger = logging.getLogger(__name__)


async def stats(message: types.Message):
    payload = message.get_args().split()

    base_log_msg = f"Admin {message.from_user.id} requested {payload} with result"

    subcommands = ["total", "file", "lang", "reqs"]

    if "total" in payload:
        total_users = User.select().where(User.is_ban == False).count()  # noqa: E712

        logger.info(f"{base_log_msg} {total_users}")

        await message.answer(total_users)

    elif "file" in payload:
        file = open(Path.cwd().joinpath("src/data/users.db"), "rb")
        input_file = types.InputFile(file)

        logger.info(f"{base_log_msg} <file>")

        await message.answer_document(input_file)

        file.close()

    elif "reqs" in payload:
        total_requests = User.select(fn.SUM(User.requests)).scalar(as_tuple=True)

        logger.info(f"{base_log_msg} {total_requests[0]}")

        await message.answer(total_requests[0])

    elif "lang" in payload:
        text = "Language Percentages:"
        top_list = []

        for lang in REPLIES["LANGS"]:
            total_users = (
                User.select().where(User.is_ban == False).count()  # noqa: E712
            )
            total_lang = User.select().where(User.language == lang).count()

            try:
                percent = total_lang / total_users
            except ZeroDivisionError:
                percent = 0.0

            top_list.append([lang, round(percent, 4)])

        for lang, per in sorted(top_list, key=lambda x: x[1], reverse=True):
            text += f"\n<pre>{lang}: {per:.2%}</pre>"

        logger.info(f"{base_log_msg} {top_list}")

        await message.answer(text=text, parse_mode="HTML")

    else:
        logger.info(f"{base_log_msg} no result.")
        await message.answer(subcommands)
