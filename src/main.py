from pathlib import Path
import logging
import json

from handlers import admin, service, callback, app, excepts
from middles import userbot

from aiogram import Bot, Dispatcher, executor
from aiogram.utils.exceptions import TelegramAPIError
from telethon import TelegramClient
import colorlog


# CONSTANTS
CONFIG = json.load(open(Path.cwd().joinpath("src/config.json")))


# LOGGING SETUP
logger = logging.getLogger()  # gets root logger
logger.setLevel(logging.DEBUG)
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(message)s"
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

debug_file = logging.FileHandler(Path.cwd().joinpath(CONFIG["LOG"]["DEBUG"]))
debug_file.setLevel(logging.DEBUG)
debug_file.setFormatter(formatter)

info_file = logging.FileHandler(Path.cwd().joinpath(CONFIG["LOG"]["INFO"]))
info_file.setLevel(logging.INFO)
info_file.setFormatter(formatter)

err_file = logging.FileHandler(Path.cwd().joinpath(CONFIG["LOG"]["ERR"]))
err_file.setLevel(logging.WARNING)
err_file.setFormatter(formatter)

[logger.addHandler(handler) for handler in [console, debug_file, info_file, err_file]]


# OBJECT INSTANTIATION
bot = Bot(token=CONFIG["AIOGRAM"]["TOKEN"])
dp = Dispatcher(bot=bot)
client = TelegramClient(
    session=str(Path.cwd().joinpath(CONFIG["TELETHON"]["SESSION"])),
    api_id=CONFIG["TELETHON"]["API_ID"],
    api_hash=CONFIG["TELETHON"]["API_HASH"],
)
client.flood_sleep_threshold = 5
client.start()


# MIDDLEWARE
middle = userbot.UserBot(client=client)
middle.add_func(app.username_reply)


# HANDLERS
dp.register_message_handler(admin.stats, commands=["stats"], user_id=CONFIG["ADMINS"])
dp.register_message_handler(service.start, commands=["start"])
dp.register_message_handler(service.lang, commands=["lang"])
dp.register_message_handler(service.help, commands=["help"])
dp.register_message_handler(service.credits, commands=["credits"])
dp.register_message_handler(app.reply_id, commands=["id"])
dp.register_message_handler(
    middle.username_reply, lambda m: any([x.type == "mention" for x in m.entities])
)
dp.register_message_handler(app.reply_with_age)

dp.register_callback_query_handler(callback.button_lang)
dp.register_inline_handler(callback.query_with_age)

dp.register_errors_handler(excepts.on_err, exception=TelegramAPIError)


# DISPATCH
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
