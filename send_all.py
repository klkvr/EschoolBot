import os
os.chdir('/home/ubuntu/EschoolBot')

from helpers import *
from models import *
from config import *
import telebot

bot = telebot.TeleBot(BOT_HASH)
TEST = 0
msg = 'Так короче, если что у вас изначально стоят квадратные скобки около "О всех". Это значит, что этот вариант УЖЕ выбран. Не нужно нажимать кучу раз на него. Я хз как объяснить, но просто на друг'

if not TEST:
    users = get_all_users()
    for user_id in users:
        try:
            bot.send_message(user_id, msg, parse_mode="HTML")
        except:
            pass
else:
    bot.send_message(410821501, msg, parse_mode="HTML")

