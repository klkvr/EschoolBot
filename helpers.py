import os
os.chdir('/home/ubuntu/EschoolBot')

from config import *
from hashlib import sha256
import redis
from telebot import types

def text_by_data(query):
    reply_markup = query.message.reply_markup['inline_keyboard']
    data = query.data
    for line in reply_markup:
        for elem in line:
            if elem['callback_data'] == data:
                return elem['text']




def hash_password(text):
    return sha256((text).encode('utf-8')).hexdigest()

def get_all_users():
    db = redis.Redis('localhost', decode_responses=True, db=REDIS_DB)
    users = set()
    for key in db.keys('user:*'):
        user_id = int(key.split(':')[1])
        users.add(user_id)
    return list(users)

def create_calculate_kb(units_calculate_data):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(*[types.InlineKeyboardButton(text=units_calculate_data[unit_id]['name'], 
        callback_data=f'calc:{units_calculate_data[unit_id]["average"]:.4f}:{units_calculate_data[unit_id]["weight"]:.4f}')
            for unit_id in units_calculate_data])
    for unit_id in units_calculate_data:
        print(f'c:{units_calculate_data[unit_id]["average"]:.4f}:{units_calculate_data[unit_id]["weight"]:.4f}')
    return kb

def calc_average_change(prev_average, prev_weight, chosen_mark, chosen_weight):
    new_weight = prev_weight
    if chosen_mark > 0:
        new_weight += chosen_weight
    else:
        new_weight -= chosen_weight
    if new_weight != 0:
        new_average = (prev_average * prev_weight + chosen_mark * chosen_weight) / new_weight
    else:
        new_average = 0
    return (round(new_average, 2), round(new_weight, 2))
