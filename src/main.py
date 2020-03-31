from pathlib import Path
import logging
import json

from handlers import admin, service, callback

from aiogram import Bot, Dispatcher, executor


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s'
)

CONFIG = json.load(open(Path.cwd().joinpath('src/config.json')))
bot = Bot(token=CONFIG['TOKEN'])
dp = Dispatcher(bot=bot)

dp.register_message_handler(admin.stats, commands=['stats'])
dp.register_message_handler(service.start, commands=['start'])
dp.register_message_handler(service.lang, commands=['lang'])
dp.register_callback_query_handler(callback.button_lang)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
