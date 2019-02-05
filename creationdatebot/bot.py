from datetime import datetime

import telebot

from config.config_handler import Config
from data.data_handler import IDData
from treeify import custom_display
import util

# debug libs
# import json
# import pprint
# pp = pprint.PrettyPrinter(indent=2)

config = Config()
data = IDData()
bot = telebot.TeleBot(token=config.SETTINGS["TOKEN"])


@bot.message_handler(commands=["start"])
def send_start(message):
    bot.send_message(message.chat.id, config.REPLIES["start"])


@bot.message_handler(content_types=["text"])
def send_age(message):
    cid = message.chat.id
    print("cid:", cid)

    # clean out the rest of the pyTelegramBotAPI's json
    json_message = message.__dict__# ["json"]
    json_message = util.clean_dict(json_message)

    # FIXME: trasnfer try except into util.py
    try:
        unix_date = data.fitted_function(message.forward_from.id)
        date = datetime.utcfromtimestamp(unix_date).strftime(
                                         config.REPLIES["age"])

        json_message["forward_from"]["registered"] = date
    except:
        unix_date = data.fitted_function(message.from_user.id)
        date = datetime.utcfromtimestamp(unix_date).strftime(
                                         config.REPLIES["age"])
        json_message["from"]["registered"] = date

    age_message = custom_display(json_message)
    bot.send_message(cid, age_message)



bot.polling()
