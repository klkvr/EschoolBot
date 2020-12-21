import redis
import json
import traceback
import os
import time
from html2text import html2text
from telegramcalendar import *
from delete_html import *
os.chdir('/home/ubuntu/EschoolBot')

import requests
from datetime import datetime
from config import *

db = redis.Redis('localhost', decode_responses=True, db=REDIS_DB)

class BotUser(object):
    def __init__(self, id):
        self.id = id
        attrs = [
                {'name': 'state', 'default': 'none'},
                {'name': 'logged_in', 'default': False},
                {'name': 'eschool_login', 'default': ''},
                {'name': 'eschool_password', 'default': ''},
                {'name': 'eschool_id', 'default': -1},
                {'name': 'real_name', 'default': ''},
                {'name': 'last_checked_mark_time', 'default': -1},
                {'name': 'notify_type', 'default': 'all'},
                {'name': 'units', 'default': {}}
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
    
    def log_in(self, save_name=0):
        response = {'logged_in': False, 'error': None, 'session': None}
        s = requests.Session()
        r = s.post('https://app.eschool.center/ec-server/login', data={'username': self.eschool_login, 'password': self.eschool_password})
        if r.status_code == 200:
            if save_name:
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
            return response
        else:
            response['logged_in'] = False
            response['error'] = 'unknown error'
            return response
    
    def get_diary_units(self, s):
        marks = requests.get(f'https://app.eschool.center/ec-server/student/getDiaryUnits/?userId={self.eschool_id}&eiId={PERIOD}', cookies=s.cookies).json()
        marks = marks['result']
        units = []
        for mark in marks:
            rating = '?'
            if 'rating' in mark:
                rating = mark['rating']
            unit_name = mark['unitName']
            unit_id = mark['unitId']
            average = round(mark.get('overMark', 0), 2)
            total = mark.get('totalMark', '')
            if total == '':
                total = str(round(average)) + '?'
            units.append({'unit_name': unit_name, 'unit_id': unit_id, 'average': average, 'total': total, 'rating': rating})
        unit_by_id = {}
        for unit in units:
            unit_by_id[unit['unit_id']] = unit['unit_name']
        self.units = unit_by_id
        return units
    
    def get_marks(self, s):
        period = []
        while len(period) == 0:
            period = requests.get(f'https://app.eschool.center/ec-server/student/getDiaryPeriod/?userId={self.eschool_id}&eiId={PERIOD}', cookies=s.cookies).json()['result']
            time.sleep(0.5 * (len(period) == 0))
        marks = []
        for elem in period:
            if 'markVal' in elem and 'mktWt' in elem:
                t = datetime.strptime(elem["markDate"], "%Y-%m-%dT%H:%M:%S").timestamp()
                marks.append({'unit_id': elem['unitId'], 'mark': elem['markVal'], 'weight': elem['mktWt'], 'name': elem['lptName'], 'time': t})
        marks.sort(key=lambda mark: mark['time'])
        return marks
    
    def get_homeworks(self, s, homework_day):
        start_date = homework_day * 1000
        end_date = start_date + 86400 * 1000 - 1
        diary = requests.get(f'https://app.eschool.center/ec-server/student/diary?userId={self.eschool_id}&d1={start_date}&d2={end_date}', cookies=s.cookies).json()['lesson']
        homeworks = []
        for elem in diary:
            unit = {'name': elem['unit']['name'], 'id': elem['unit']['id']}
            for p in elem['part']:
                if p['name'] == 'Дом. задание' or p['name'] == 'Контрольное д/з':
                    for variant in p['variant']:
                        homeworks.append({'unit': unit, 'text': delete_html(html2text(variant.get('text', ''), bodywidth=0)), 'files': [{'id': f['id'], 'name': f['fileName']} for f in variant['file']]})
        return homeworks
    
    def get_conferences(self, s, conferences_day):
        start_date = conferences_day * 1000
        end_date = start_date + 86400 * 1000 - 1
        diary = requests.get(f'https://app.eschool.center/ec-server/student/diary?userId={self.eschool_id}&d1={start_date}&d2={end_date}', cookies=s.cookies).json()['lesson']
        conferences = []
        for elem in diary:
            if 'meet' in elem and 'inviteText' in elem['meet']:
                text = elem['meet']['inviteText']
                if 'https:' in text:
                    text = text[text.find('https:'):]
                    text = text[:text.find('\n')]
                conference = {'unit': elem['unit']['name'], 'link': text}
                if conference not in conferences:
                    conferences.append(conference)
        return conferences
    
    def get_lessons(self, s, lessons_day):
        start_date = lessons_day * 1000
        end_date = start_date + 86400 * 1000 - 1
        diary = requests.get(f'https://app.eschool.center/ec-server/student/diary?userId={self.eschool_id}&d1={start_date}&d2={end_date}', cookies=s.cookies).json()['lesson']
        lessons = [''] * 8
        for elem in diary:
            num = elem['numInDay']
            unit = elem['unit']['name']
            if lessons[num] == '':
                lessons[num] = unit
        return lessons
    def get_class(self, s):
        groups = s.get(f'https://app.eschool.center/ec-server/usr/groupByUser?dt={int(time.time())*1000}&userId={self.eschool_id}').json()
        for group in groups:
            if 'groupTypeName' in group and group['groupTypeName'] in ["Классы школы", 'School classes']:
                return group["groupName"]

