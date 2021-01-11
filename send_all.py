import os
os.chdir('/home/ubuntu/EschoolBot')

from helpers import *
from models import *
from config import *
import telebot

bot = telebot.TeleBot(BOT_HASH)
TEST = 0
msg = 'всем ку ескул опять забанил айпишник моего сервера, так что пока я не улажу этот вопрос с их поддержкой или не перееду на другой сервер, бот лежит🤷‍♂️'
if not TEST:
    users = get_all_users()
    for user_id in users:
        try:
            bot.send_message(user_id, msg, parse_mode="HTML")
        except:
            pass
else:
    bot.send_message(410821501, msg, parse_mode="HTML")

