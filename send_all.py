import os
os.chdir('/home/ubuntu/EschoolBot')

from helpers import *
from models import *
from config import *
import telebot

bot = telebot.TeleBot(BOT_HASH)
TEST = 1
msg = 'По многочисленным просьбам добавил функцию выбора оценок, о которых будут приходить уведомления. Можно получать все оценки, только хорошие, или не получать вообще.\n\nИспользуйте команду /notify_settings'

if not TEST:
    users = get_all_users()
    for user_id in users:
        bot.send_message(user_id, msg, parse_mode="HTML")
else:
    bot.send_message(410821501, msg, parse_mode="HTML")

