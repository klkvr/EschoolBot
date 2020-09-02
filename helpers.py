import os
os.chdir('/home/ubuntu/EschoolBot')

from config import *
from hashlib import sha256
import redis

def hash_password(text):
    return sha256((text).encode('utf-8')).hexdigest()

def get_all_users():
    db = redis.Redis('localhost', decode_responses=True, db=REDIS_DB)
    users = set()
    for key in db.keys('user:*'):
        user_id = int(key.split(':')[1])
        users.add(user_id)
    return list(users)