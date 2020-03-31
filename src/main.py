from pathlib import Path
import logging
import json

from handlers import admin

from aiogram import Bot, Dispatcher, executor


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(message)s'
)

config = json.load(open(Path.cwd().joinpath('config.json')))
bot = Bot(token=config['TOKEN'])
dp = Dispatcher(bot=bot)

dp.register_message_handler(admin.stats, commands=['stats'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
