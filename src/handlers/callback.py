"""
Handlers for dealing with callbacks
"""
import json, pathlib  # noqa: E401
from aiogram import Bot, types
from process.database import User


REPLIES = json.load(open(pathlib.Path.cwd().joinpath('src/ui/replies.json')))


async def button_lang(query: types.CallbackQuery):
    user = User.get(User.user_id == query.from_user.id)
    bot = Bot.get_current()

    # bad clients can send arbitrary callback data
    if getattr(query, 'data', None) not in REPLIES['LANGS']:
        return

    user.language = query.data
    user.save()

    await query.answer()
    await bot.edit_message_text(
        text=REPLIES['lang_success'][query.data],
        message_id=query.message.message_id,
        chat_id=query.from_user.id
    )
