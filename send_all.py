import os
os.chdir('/home/ubuntu/EschoolBot')

from helpers import *
from models import *
from config import *
import telebot

bot = telebot.TeleBot(BOT_HASH)
TEST = 1
msg = 'Все срочно подписываемся на лучшие паблики вк!!!\n\nhttps://vk.com/it_seems_art\nhttps://vk.com/club198528337'

if not TEST:
    users = get_all_users()
    for user_id in users:
        try:
            bot.send_message(user_id, msg, parse_mode="HTML")
        except:
            pass
else:
    bot.send_message(410821501, msg, parse_mode="HTML")

