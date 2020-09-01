import redis
import json
import requests
from config import *

db = redis.Redis('localhost', decode_responses=True, db=1)

class BotUser(object):
    def __init__(self, id):
        self.id = id
        attrs = [
                {'name': 'state', 'default': 'none'},
                {'name': 'logged_in', 'default': False},
                {'name': 'eschool_login', 'default': ''},
                {'name': 'eschool_password', 'default': ''},
                {'name': 'real_name', 'default': ''}
                ]
        for attr in attrs:
            if db.exists(f'user:{id}:{attr["name"]}'):
                self.__setattr__(attr["name"], json.loads(db.get(f'user:{id}:{attr["name"]}')))
            else:
                self.__setattr__(attr["name"], attr["default"])
    def __setattr__(self, name, value):
        if name in ['id']:
            self.__dict__[name] = value
        else:
            self.__dict__[name] = value
            db.set(f'user:{self.id}:{name}', json.dumps(value))
    
    def log_in(self):
        response = {'logged_in': False, 'error': None, 'session': None}
        s = requests.Session()
        r = s.post('https://app.eschool.center/ec-server/login', data={'username': self.eschool_login, 'password': self.eschool_password})
        if r.status_code == 200:
            name = requests.get('https://app.eschool.center/ec-server/state', cookies=s.cookies).json()['user']['currentPosition']
            self.real_name = name['prsFio']
            if name['posName'] == 'Родитель':
                child = requests.get(f'https://app.eschool.center/ec-server/profile/{name["userId"]}/children', cookies=s.cookies).json()[0]
                self.eschool_id = int(child['userId'])
            elif name['posName'] == 'Ученик':
                self.eschool_id = int(name['userId'])
            else:
                response['logged_in'] = False
                response['error'] = 'teacher'
                return response
            response['session'] = s
            response['logged_in'] = True
            self.logged_in = True
            return response
        else:
            response['logged_in'] = False
            response['error'] = 'unknown error'
            return response
    
    def get_period_marks(self, s):
        marks = requests.get(f'https://app.eschool.center/ec-server/student/getDiaryUnits/?userId={self.eschool_id}&eiId={PERIOD}', cookies=s.cookies).json()
        marks = marks['result']
        return_value = []
        for mark in marks:
            if 'overMark' in mark and 'totalMark' in mark:
                unit = mark['unitName']
                average = round(mark['overMark'], 2)
                total = mark['totalMark']
                if total == '':
                    total = str(round(average)) + '?'
                return_value.append({'unit': unit, 'average': average, 'total': total})
        return return_value

