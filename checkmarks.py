import requests, os
import telebot, time, codecs


os.chdir('EschoolBot')
period_const = '145630'
def save_marks(marks):
    f = codecs.open('prevmarks.txt', 'w')
    print(marks, file=f)
    f.close()


bot = telebot.TeleBot(open('bothash.txt', 'r').readline().rstrip())
users_data = {int(i.rstrip().split()[0]): {'login_data':
                    {'username': i.rstrip().split()[1:-2], 'password': i.rstrip().split()[-2]},
                    'id': int(i.rstrip().split()[-1])} for i in open('pal.txt', 'r')}
for i in users_data:
    s = ''
    for j in users_data[i]['login_data']['username']:
        s += j + ' '
    s = s[:-1]
    users_data[i]['login_data']['username'] = s
try:
    prev_marks = eval(codecs.open('prevmarks.txt', 'r').readline().rstrip())
except:
    prev_marks = {}
marks = {}
for user in users_data:
    try:
        marks[user] = []
        s = requests.session()
        if s.post('https://app.eschool.center/ec-server/login', data=users_data[user]['login_data']).status_code == 200:
            getunits = requests.get('https://app.eschool.center/ec-server/student/getDiaryUnits/?userId=' + str(users_data[user]['id']) + '&eiId=' + period_const, cookies=s.cookies)
            while getunits.status_code != 200:
                getunits = requests.get('https://app.eschool.center/ec-server/student/getDiaryUnits/?userId=' + str(users_data[user]['id']) + '&eiId=' + period_const, cookies=s.cookies)
                time.sleep(2)
            getunits = getunits.json()['result']
            units = {i['unitId']: i['unitName'] for i in getunits}
            averages = {}
            for i in getunits:
                if 'overMark' in i:
                    averages[i['unitName']] = i['overMark']
                else:
                    averages[i['unitName']] = 0
            period = requests.get('https://app.eschool.center/ec-server/student/getDiaryPeriod/?userId=' + str(users_data[user]['id']) + '&eiId=' + period_const, cookies=s.cookies)
            while period.status_code != 200 or len(period.json()['result']) == 0:
                period = requests.get('https://app.eschool.center/ec-server/student/getDiaryPeriod/?userId=' + str(users_data[user]['id']) + '&eiId=' + period_const, cookies=s.cookies)
                time.sleep(2)
            period = period.json()['result']
            for i in period:
                if 'markVal' in i:
                    marks[user].append([i['markId'], {'id': i['markId'], 'unit': units[i['unitId']], 'val': i['markVal'], 'weight': i['mktWt'], 'name': i['lptName']}])
            marks[user].sort()
            marks[user] = marks[user][::-1]
            if user in prev_marks:
                if marks[user] != prev_marks[user]:
                    for mark in marks[user]:
                        if mark not in prev_marks[user]:
                            flag = 0
                            for prev_mark in prev_marks[user]:
                                if prev_mark[0] == mark[0]:
                                    try:
                                        bot.send_message(user, 'Оценка изменена:\n*' + mark[1]['unit'] + '*\n_' + mark[1]['name'] + '_\nЗначение: ' + str(prev_mark[1]['val']) + ' → ' + str(mark[1]['val']) + '\nКоэффициент: ' + str(mark[1]['weight']) + '\nСредний балл: ' + str(round(averages[mark[1]['unit']], 2)), parse_mode="Markdown")
                                        flag = 1
                                    except:
                                        flag = 1
                                    save_marks(prev_marks)
                            if not flag:
                                try:
                                    bot.send_message(user, 'Новая оценка:\n*' + mark[1]['unit'] + '*\n_' + mark[1]['name'] + '_\nЗначение: ' + str(mark[1]['val']) + '\nКоэффициент: ' + str(mark[1]['weight']) + '\nСредний балл: ' + str(round(averages[mark[1]['unit']], 2)), parse_mode="Markdown")
                                except:
                                    flag = flag
                                save_marks(prev_marks)
                    for prev_mark in prev_marks[user]:
                        if prev_mark not in marks[user]:
                            flag = 0
                            for mark in marks[user]:
                                if prev_mark[0] == mark[0]:
                                    flag = 1
                            if not flag and not prev_mark == prev_marks[user][0]:
                                try:
                                    bot.send_message(user, 'Оценка удалена:\n*' + prev_mark[1]['unit'] + '*\n_' + prev_mark[1]['name'] + '_\nЗначение: ' + str(prev_mark[1]['val']) + '\nКоэффициент: ' + str(prev_mark[1]['weight']) + '\nСредний балл: ' + str(round(averages[prev_mark[1]['unit']], 2)), parse_mode="Markdown")
                                except:
                                    flag = flag
                                save_marks(prev_marks)
            prev_marks[user] = marks[user]
            save_marks(prev_marks)
        else:
            print('err')
    except:
        bot.send_message('@eschool239boterrors', traceback.format_exc())
save_marks(prev_marks)
