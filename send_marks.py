import os
os.chdir('/home/ubuntu/EschoolBot')

from config import *
from models import *
from helpers import *
import telebot
import time

bot = telebot.TeleBot(BOT_HASH)

users = get_all_users()
for user_id in users:
    try:
        user = BotUser(user_id)
        if user.logged_in:
            log_in_attempt = user.log_in()
            time.sleep(0.5)
            if log_in_attempt['logged_in']:
                s = log_in_attempt['session']
                marks = user.get_marks(s)
                if len(marks) != 0:
                    time.sleep(0.5)
                    units = user.get_diary_units(s)
                    unit_by_id = {}
                    for unit in units:
                        unit_by_id[unit['unit_id']] = {'name': unit['unit_name'], 'average': unit['average']}
                    if user.last_checked_mark_time != -1:
                        for mark in marks:
                            if mark['time'] > user.last_checked_mark_time:
                                msg = f'Новая оценка\n<b>{unit_by_id[mark["unit_id"]]["name"]}</b>\n<i>{mark["name"]}</i>\nЗначение: {mark["mark"]}\nКоэффициент: {mark["weight"]}\nСредний балл: {unit_by_id[mark["unit_id"]]["average"]}'
                                bot.send_message(user.id, msg, parse_mode="HTML")
                    user.last_checked_mark_time = marks[-1]["time"]
    except telebot.apihelper.ApiException as e:
        print('bot was blocked by the user' in str(e))
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())
    time.sleep(0.5)
