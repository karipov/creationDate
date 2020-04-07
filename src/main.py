from pathlib import Path
import logging
import json

from handlers import admin, service, callback, app, excepts

from aiogram import Bot, Dispatcher, executor
from aiogram.utils.exceptions import TelegramAPIError

CONFIG = json.load(open(Path.cwd().joinpath('src/config.json')))

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(message)s',
    filename=CONFIG['LOGFILE'],
    filemode='w'
)

bot = Bot(token=CONFIG['TOKEN'])
dp = Dispatcher(bot=bot)

# Message handlers
dp.register_message_handler(
    admin.stats, commands=['stats'], user_id=CONFIG['ADMINS']
)
dp.register_message_handler(service.start, commands=['start'])
dp.register_message_handler(service.lang, commands=['lang'])
dp.register_message_handler(service.help, commands=['help'])
dp.register_message_handler(service.credits, commands=['credits'])
dp.register_message_handler(excepts.err_expected, commands=['err'])
dp.register_message_handler(app.reply_with_age)

# Callback handlers
dp.register_callback_query_handler(callback.button_lang)
dp.register_inline_handler(callback.query_with_age)

# Error handlers
dp.register_errors_handler(excepts.on_err, exception=TelegramAPIError)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
