import os
os.chdir('/home/ubuntu/EschoolBot')

from helpers import *
from models import *
from config import *
import telebot

bot = telebot.TeleBot(BOT_HASH)
TEST = 0
msg = 'так ребята теперь это чудо мой проект по инфе, и мне будут ставить крутые оценки за то что я буду добавлять новые фичи, так что если у вас есть идея для новой функции в боте, то отпишите мне @klkvr'
if not TEST:
    users = get_all_users()
    for user_id in users:
        try:
            bot.send_message(user_id, msg, parse_mode="HTML")
        except:
            pass
else:
    bot.send_message(410821501, msg, parse_mode="HTML")

