from datetime import datetime
from os import environ

import telebot
from flask import Flask, request

from config.config_handler import Config
from data.data_handler import IDData
import util

## FIXME: ADD LOGGING
# Class instances
config = Config()
data = IDData()
bot = telebot.TeleBot(token=config.SETTINGS["TOKEN"])
server = Flask(__name__)


# flask server stuff
@server.route('/' + config.SETTINGS["TOKEN"], methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "", 200


@server.route("/")
def webhook():
    bot.remove_webhook() # if you don't remove webhook, it some times errors
    bot.set_webhook(url=config.SETTINGS["HEROKU"] + config.SETTINGS["TOKEN"])
    return "Success", 200


# bot message handlers
@bot.message_handler(commands=["start"])
def send_start(message):
    bot.send_message(message.chat.id, config.REPLIES["start"])


@bot.message_handler(content_types=["text"])
def send_age(message):
    """
    Sends the tree formatted json message with the approximate creation date
    """
    cid = message.chat.id
    json_message = util.msg_to_dict(message)

    # checks if a message has been forwarded
    if util.check_forward(message):
        unix_date_forwd = data.fitted_function(message.forward_from.id)
        date_forwd = util.cvt_time(unix_date_forwd, config.REPLIES["age"])
        json_message["forward_from"]["registered"] = date_forwd

    unix_date = data.fitted_function(message.from_user.id)
    date = util.cvt_time(unix_date, config.REPLIES["age"])
    json_message["from"]["registered"] = date

    age_message = util.custom_display(json_message)
    bot.send_message(cid, age_message)



if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))
