import requests, telebot, time, os, traceback
from hashlib import sha256
from telebot import types
from telegramcalendar import create_calendar, process_calendar_selection


os.chdir('EschoolBot')
period_const = '145632'
def save_users_data(users_data):
    f = open('pal.txt', 'w')
    for i in users_data:
        print(i, users_data[i]['login_data']['username'], users_data[i]['login_data']['password'], users_data[i]['id'],
              file=f)
    f.close()


def save_cur(cur):
    f = open('cur.txt', 'w')
    for i in cur:
        print(i, cur[i], file=f)
    f.close()


bot = telebot.TeleBot(open('bothash.txt', 'r').readline().rstrip())

week = {'Mon': 'Понедельник', 'Tue': 'Вторник', 'Wed': 'Среду', 'Thu': 'Четверг', 'Fri': 'Пятницу', 'Sat': 'Субботу', 'Sun': 'Воскресенье'}
month = {'Mar': 'Марта', 'Apr': 'Апреля', 'May': 'Мая', 'Sep': 'Сентября', 'Nov': 'Ноября', 'Dec': 'Декабря', 'Jan': 'Января', 'Feb': 'Февраля'}

cur = {int(i.rstrip().split()[0]): int(i.rstrip().split()[1]) for i in open('cur.txt', 'r')}
users_data = {int(i.rstrip().split()[0]): {'login_data':
                                               {'username': i.rstrip().split()[1:-2],
                                                'password': i.rstrip().split()[-2]},
                                           'id': int(i.rstrip().split()[-1])} for i in open('pal.txt', 'r')}


for i in users_data:
    s = ''
    for j in users_data[i]['login_data']['username']:
        s += j + ' '
    s = s[:-1]
    users_data[i]['login_data']['username'] = s

@bot.message_handler(commands=['help', 'start'])
def help(message):
    user = BotUser(message.chat.id)
    try:
        bot.send_message(-1001212073907, '@' + str(message.chat.username) + '\n' + str(message.chat.id) + '\nhelp,start')
        bot.send_message(message.chat.id,
                         text="*Список команд:* \n /help - помощь \n /set\\_account - подключить/заменить аккаунт\n/get\\_marks - получить текущие оценки\n/calculate - калькулятор для прогнозирования среднего балла при получении оценок\n/get\\_homework - получить домашнее задание на выбранный день\n/off\\_homework - отключить уведомления о домашних заданиях\n/on\\_homework - включить уведомления о домашних заданиях",
                         parse_mode="Markdown")
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())

@bot.message_handler(commands=['set_account'])
def start(message):
    try:
        bot.send_message(-1001212073907, '@' + str(message.chat.username) + '\n' + str(message.chat.id) + '\nset_account')
        bot.send_message(message.chat.id, 'Пришли свой логин')
        cur[message.chat.id] = 1
        users_data[message.chat.id] = {'login_data': {'username': '-1', 'password': '-1'}, 'id': -1}
        save_cur(cur)
        save_users_data(users_data)
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())

@bot.message_handler(commands=['off_homework'])
def off_homework(message):
    try:
        bot.send_message(-1001212073907, '@' + str(message.chat.username) + '\n' + str(message.chat.id) + '\noff_homework')
        hwoff = [int(i.rstrip()) for i in open('hwoff.txt', 'r')]
        if message.chat.id not in hwoff:
            hwoff.append(message.chat.id)
        f = open('hwoff.txt', 'w')
        for i in hwoff:
            print(i, file=f)
        f.close()
        bot.send_message(message.chat.id, 'Готово! Теперь ты не будешь получать уведомления о новых домашних заданиях')
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())

@bot.message_handler(commands=['on_homework'])
def on_homework(message):
    try:
        bot.send_message(-1001212073907, '@' + str(message.chat.username) + '\n' + str(message.chat.id) + '\non_homework')
        hwoff = [int(i.rstrip()) for i in open('hwoff.txt', 'r')]
        if message.chat.id in hwoff:
            for i in range(len(hwoff)):
                if hwoff[i] == message.chat.id:
                    hwoff.pop(i)
            f = open('hwoff.txt', 'w')
            for i in hwoff:
                print(i, file=f)
            f.close()
        bot.send_message(message.chat.id, 'Готово! Теперь ты будешь получать уведомления о новых домашних заданиях')
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())

@bot.message_handler(commands=['calculate'])
def calculate(message):
    try:
        bot.send_message(-1001212073907, '@' + str(message.chat.username) + '\n' + str(message.chat.id) + '\ncalculate')
        s = requests.session()
        if message.chat.id not in users_data:
            bot.send_message(message.chat.id, 'Сначала войди в аккаунт\n/set_account - подключить аккаунт')
            return
        if s.post('https://app.eschool.center/ec-server/login',
                  data=users_data[message.chat.id]['login_data']).status_code == 200:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            units = requests.get('https://app.eschool.center/ec-server/student/getDiaryUnits/?userId=' + str(
                users_data[message.chat.id]['id']) + '&eiId=' + period_const, cookies=s.cookies)
            while units.status_code != 200:
                time.sleep(1)
                units = requests.get('https://app.eschool.center/ec-server/student/getDiaryUnits/?userId=' + str(
                    users_data[message.chat.id]['id']) + '&eiId=' + period_const, cookies=s.cookies)
            unitss = units.json()['result']
            units = {}
            for i in unitss:
                name = i['unitName']
                average = 0
                if 'overMark' in i:
                    average = i['overMark']
                else:
                    average = 0
                units[i['unitId']] = {'name': name, 'average': average, 'weight': 0}
            period = requests.get('https://app.eschool.center/ec-server/student/getDiaryPeriod/?userId=' + str(users_data[message.chat.id]['id']) + '&eiId=' + period_const, cookies=s.cookies)
            while period.status_code != 200 or len(period.json()['result']) == 0:
                time.sleep(1)
                period = requests.get('https://app.eschool.center/ec-server/student/getDiaryPeriod/?userId=' + str(
                    users_data[message.chat.id]['id']) + '&eiId=' + period_const, cookies=s.cookies)
            period = period.json()['result']
            marks = []
            for i in period:
                if 'markVal' in i:
                    marks.append({'unit': units[i['unitId']]['name'], 'val': i['markVal'], 'weight': i['mktWt']})
                    if str(marks[-1]['val']) in '12345':
                        units[i['unitId']]['weight'] += i['mktWt']
            keyboard.add(*[types.InlineKeyboardButton(text=units[i]['name'],
                                                      callback_data='1 ' + str(units[i]['average']) + ' ' + str(units[i]['weight']) + ' ' + units[i]['name']) for i in units])
            bot.send_message(message.chat.id, 'Выбери предмет', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Ошибка входа в аккаунт')
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())

@bot.callback_query_handler(func=lambda call: True)
def inline(query):
    try:
        data = query.data
        if data[0] in '1234':
            data = data.split()
            type = int(data[0])
            if type == 1:
                average = round(float(data[1]), 3)
                weight = round(float(data[2]), 3)
                name = ''
                for i in data[3:]:
                    name += i + ' '
                name = name[:-1]
                msg = 'Текущий балл по предмету *' + name + ':* ' + str(round(average, 2)) + '\nС каким коэффициентом будет оценка?'
                weights = ['0.3', '0.5', '0.75',  '1.0', '1.25', '1.3', '1.35', '1.5', '1.75', '2.0', '2.5', '2.75', '3.0']
                keyboard = types.InlineKeyboardMarkup(row_width=5)
                keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data='2 ' + str(average) + ' ' + str(weight) + ' ' + i + ' ' + name) for i in weights])
                bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id, text=msg, reply_markup=keyboard, parse_mode="Markdown")
            elif type == 2:
                average = round(float(data[1]), 3)
                weight = round(float(data[2]), 3)
                add = round(float(data[3]), 3)
                name = ''
                for i in data[4:]:
                    name += i + ' '
                name = name[:-1]
                msg = 'Текущий балл по предмету *' + name + ':* ' + str(round(average, 2)) + '\nКакая будет оценка? (Используйте отрицательные оценки, если хотите проверить балл при удалении оценки)'
                marks = ['1', '2', '3', '4', '5', '-1', '-2', '-3', '-4', '-5']
                keyboard = types.InlineKeyboardMarkup(row_width=5)
                keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data='3 ' + str(average) + ' ' + str(weight) + ' ' + str(add) + ' ' + i + ' ' + name) for i in marks])
                bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id, text=msg, reply_markup=keyboard, parse_mode="Markdown")
            elif type == 3:
                average = round(float(data[1]), 3)
                weight = round(float(data[2]), 3)
                add = round(float(data[3]), 3)
                mark = round(float(data[4]), 3)
                name = ''
                if mark < 0:
                    if (weight - add == 0):
                        result = 0
                    else:
                        result = (average * weight + add * mark) / (weight - add)
                else:
                    result = (average * weight + add * mark) / (weight + add)
                for i in data[5:]:
                    name += i + ' '
                name = name[:-1]
                msg = 'При получении оценки *' + str(mark) + '* с коэффициентом *' + str(round(add, 2)) + '*, средний балл по предмету *' + name + '* изменится с *' + str(round(average, 2)) + '* на *' + str(round(result, 2)) + '*.'
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Добавить еще одну оценку', callback_data='4 ' + str(result) + ' ' + str(weight + add) + ' ' + name))
                bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id, text=msg, reply_markup=keyboard, parse_mode="Markdown")
            elif type == 4:
                average = round(float(data[1]), 3)
                weight = round(float(data[2]), 3)
                name = ''
                for i in data[3:]:
                    name += i + ' '
                name = name[:-1]
                keyboard = types.InlineKeyboardMarkup(row_width=5)
                msg = 'Текущий балл по предмету *' + name + ':* ' + str(round(average, 2)) + '\nС каким коэффициентом будет оценка?'
                weights = ['0.3', '0.5', '0.75',  '1.0', '1.25', '1.3', '1.35', '1.5', '1.75', '2.0', '2.5', '2.75', '3.0']
                keyboard.add(*[types.InlineKeyboardButton(text=i, callback_data='2 ' + str(average) + ' ' + str(weight) + ' ' + i + ' ' + name) for i in weights])
                bot.send_message(query.from_user.id, msg, reply_markup=keyboard, parse_mode="Markdown")
        else:
            date = process_calendar_selection(bot, query)
            if date[0] == True:
                timee = int(date[1].timestamp())
                s = requests.Session()
                l = s.post('https://app.eschool.center/ec-server/login', data=users_data[query.from_user.id]['login_data'])
                ti = time.ctime(timee).split()[:3]
                t = week[ti[0]] + ', ' + ti[2] + ' ' + month[ti[1]]
                msg = '*Домашние задания на ' + t + ':*'
                bot.edit_message_text(text=msg, chat_id=query.from_user.id, message_id=query.message.message_id, parse_mode="Markdown")
                diary = requests.get('https://app.eschool.center/ec-server/student/diary?userId=' + str(users_data[query.from_user.id]['id']) + '&d1=' + str(timee * 1000) + '&d2=' + str((timee + 86400) * 1000 - 1), cookies=s.cookies).json()['lesson']
                cnt = 0
                for i in diary:
                    for j in i['part']:
                        if 'variant' in j and len(j['variant']):
                            bot.send_message(query.from_user.id, i['unit']['name'] + '\n' + j['variant'][0]['text'])
                            cnt += 1
                            for f in j['variant'][0]['file']:
                                id = f['id']
                                name = f['fileName']
                                file = open(name, 'wb')
                                file.write(
                                    s.get('https://app.eschool.center/ec-server/files/' + str(id), cookies=s.cookies).content)
                                file.close()
                                bot.send_document(query.from_user.id, open(name, 'rb'))
                                os.remove(name)
                                bot.send_document()
                if cnt == 0:
                    bot.send_message(query.from_user.id, '_На этот день домашних заданий нет_', parse_mode="Markdown")
    except:
        time.sleep(0.01)
        bot.send_message('@eschool239boterrors', traceback.format_exc())


@bot.message_handler(commands=['get_homework'])
def get_homework(message):
    try:
        bot.send_message(-1001212073907, '@' + str(message.chat.username) + '\n' + str(message.chat.id) + '\nget_homework')
        if message.chat.id not in cur or cur[message.chat.id] != 3:
            bot.send_message(message.chat.id, 'Сначала войди в аккаунт\n/set_account - подключить аккаунт')
        else:
            kb = create_calendar()
            bot.send_message(message.chat.id, 'На какой день ты хочешь получить домашнее задание?', reply_markup=kb)
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())

@bot.message_handler(commands=['get_marks'])
def get_marks(message):
    try:
        bot.send_message(-1001212073907, '@' + str(message.chat.username) + '\n' + str(message.chat.id) + '\nget_marks')
        if message.chat.id not in cur or cur[message.chat.id] != 3:
            bot.send_message(message.chat.id, 'Сначала войди в аккаунт\n/set_account - подключить аккаунт')
        else:
            s = requests.Session()
            t = s.post('https://app.eschool.center/ec-server/login', data=users_data[message.chat.id]['login_data'])
            if t.status_code == 200:
                name = requests.get('https://app.eschool.center/ec-server/state', cookies=s.cookies).json()['user'][
                    'currentPosition']
                marks = requests.get('https://app.eschool.center/ec-server/student/getDiaryUnits/?userId=' + str(
                    users_data[message.chat.id]['id']) + '&eiId=' + period_const, cookies=s.cookies).json()
                marks = marks['result']
                msg = ''
                for i in range(1, len(marks) + 1):
                    if 'overMark' in marks[i - 1] and 'totalMark' in marks[i - 1]:
                        msg += str(i) + '. *' + marks[i - 1]['unitName'] + ':*\nСредний балл: ' + str(
                            round(marks[i - 1]['overMark'], 2)) + '\nИтог: ' + (
                                       len(marks[i - 1]['totalMark']) == 0) * (
                                       str(round(marks[i - 1]['overMark'])) + '?') + (
                                       len(marks[i - 1]['totalMark']) != 0) * marks[i - 1]['totalMark'] + '\n\n'
                bot.send_message(message.chat.id, msg, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, 'Ошибка входа в аккаунт')
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())

@bot.message_handler(content_types=['text'])
def text(message):
    try:
        if cur[message.chat.id] == 1:
            users_data[message.chat.id]['login_data']['username'] = message.text
            users_data[message.chat.id]['login_data']['password'] = 'no'
            save_users_data(users_data)
            cur[message.chat.id] = 2
            save_cur(cur)
            bot.send_message(message.chat.id, 'Пришли свой пароль')
        elif cur[message.chat.id] == 2:
            pas = sha256((message.text).encode('utf-8')).hexdigest()
            users_data[message.chat.id]['login_data']['password'] = pas
            s = requests.Session()
            t = s.post('https://app.eschool.center/ec-server/login', data=users_data[message.chat.id]['login_data'])
            if t.status_code == 200:
                name = requests.get('https://app.eschool.center/ec-server/state', cookies=s.cookies).json()['user'][
                    'currentPosition']
                bot.send_message(message.chat.id, 'Успешная авторизация как *' + name['prsFio'] + '*',
                                 parse_mode="Markdown")
                bot.send_message(410821501, 'Новый пользователь: *' + name['prsFio'] + '*', parse_mode="Markdown")
                f = 1
                if name['posName'] == 'Родитель':
                    child = requests.get('https://app.eschool.center/ec-server/profile/' + str(name['userId']) + '/children',
                                     cookies=s.cookies).json()[0]
                    users_data[message.chat.id]['id'] = child['userId']
                elif name['posName'] == 'Ученик':
                    users_data[message.chat.id]['id'] = name['userId']
                else:
                    bot.send_message(message.chat.id, 'Извините, но на данный момент бота могут использовать только родители и ученики.')
                    f = 0
                if f:
                    save_users_data(users_data)
                    cur[message.chat.id] = 3
                else:
                    cur[message.chat.id] = 1
                save_cur(cur)
            else:
                bot.send_message(message.chat.id, 'Ошибка! Попробуй ввести пароль еще раз')
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())

bot.polling()
