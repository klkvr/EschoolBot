import os
os.chdir('/home/ubuntu/EschoolBot')

import telebot
from telebot import types
from config import *
from helpers import *
from models import *
from templates import *

bot = telebot.TeleBot(BOT_HASH)


def send_period_marks(user_id, marks):
    user = BotUser(user_id)
    msg = ''
    for i in range(len(marks)):
        msg += f'{i+1}. <b>{marks[i]["unit_name"]}:</b>\nСредний балл: {marks[i]["average"]}\nИтог: {marks[i]["total"]}\n\n'
    bot.send_message(user.id, msg, parse_mode="HTML")

@bot.message_handler(commands=['start', 'help'])
def start(message):
    user = BotUser(message.chat.id)
    user.state = 'none'
    bot.send_message(user.id, start_message, parse_mode="HTML")

@bot.message_handler(commands=['set_account'])
def set_account(message):
    user = BotUser(message.chat.id)
    bot.send_message(user.id, enter_login)
    user.state = 'enter_login'

"""
@bot.message_handler(commands=['calculate'])
def calculate(message):
    user = BotUser(message.chat.id)
    user.state = 'none'
    bot.send_message(user.id, start_message, parse_mode="HTML")
    if not user.logged_in:
        bot.send_message(user.id, log_in_first)
    else:
        log_in_attempt = user.log_in()
        if log_in_attempt['logged_id']:
            period_marks = user.get_diary_units(log_in_attempt['session'])
"""



@bot.message_handler(commands=['get_marks'])
def get_marks(message):
    try:
        user = BotUser(message.chat.id)
        if not user.logged_in:
            bot.send_message(user.id, log_in_first)
        else:
            message_to_delete = bot.send_message(user.id, getting_marks)
            log_in_attempt = user.log_in()
            if log_in_attempt['logged_in']:
                marks = user.get_diary_units(log_in_attempt['session'])
                send_period_marks(user.id, marks)
            else:
                bot.send_message(user.id, error_logging_in)
            bot.delete_message(user.id, message_to_delete.message_id)
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())

@bot.message_handler(content_types=['text'])
def text(message):
    try:
        user = BotUser(message.chat.id)
        text = message.text
        if user.state == 'enter_login':
            user.eschool_login = text
            bot.send_message(user.id, enter_password)
            user.state = 'enter_password'
        elif user.state == 'enter_password':
            user.eschool_password = hash_password(text)
            message_to_delete = bot.send_message(user.id, logging_in)
            log_in_attempt = user.log_in(1)
            if log_in_attempt['logged_in']:
                bot.send_message(user.id, success_login_format.format(user=user), parse_mode="HTML")
                bot.send_message(410821501, f'Новый пользователь: {user.real_name}')
                user.logged_in = True
            elif log_in_attempt['error'] == 'teacher':
                bot.send_message(user.id, sorry_for_teachers)
            else:
                bot.send_message(user.id, unknown_error)
            bot.delete_message(user.id, message_to_delete.message_id)
            user.state = 'none'
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())
bot.polling()