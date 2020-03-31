import requests, time, codecs, traceback


def save_diary(diary):
    f = codecs.open('prevdiary.txt', 'w')
    print(diary, file=f)
    f.close()


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
try:
    prev_diary = eval(codecs.open('prevdiary.txt', 'r').readline().rstrip())
except:
    prev_diary = {}
diary = {}
for user in users_data:
    try:
        diary[user] = {}
        s = requests.Session()
        enter = s.post('https://app.eschool.center/ec-server/login', data=users_data[user]['login_data'])
        attempts = 0
        while enter.status_code != 200 and attempts < 3:
            time.sleep(1)
            enter = s.post('https://app.eschool.center/ec-server/login', data=users_data[user]['login_data'])
            attempts += 1

        if enter.status_code == 200:
            timee = (int(time.time()) // 86400) * 86400
            getdiary = requests.get('https://app.eschool.center/ec-server/student/diary?userId=' + str(users_data[user]['id']) + '&d1=' + str(timee * 1000) + '&d2=' + str((timee + 86400 * 14) * 1000 - 1), cookies=s.cookies).json()['lesson']
            print('https://app.eschool.center/ec-server/student/diary?userId=' + str(users_data[user]['id']) + '&d1=' + str(timee * 1000) + '&d2=' + str((timee + 86400 * 14) * 1000 - 1))
            for i in getdiary:
                date = i['date'] // 1000
                unit = i['unit']['name']
                if date not in diary[user]:
                    diary[user][date] = {}
                if unit not in diary[user][date]:
                    diary[user][date][unit] = []
                for j in i['part']:
                    for elem in j['variant']:
                        if 'text' in elem:
                            diary[user][date][unit].append({'text': elem['text'], 'file': elem['file']})
                        else:
                            diary[user][date][unit].append({'text': '', 'file': elem['file']})
            if user in prev_diary:
                if diary[user] != prev_diary[user]:
                    for date in diary[user]:
                        if date in prev_diary[user]:
                            for unit in diary[user][date]:
                                if unit in prev_diary[user][date]:
                                    for hw in diary[user][date][unit]:
                                        if hw not in prev_diary[user][date][unit]:
                                            print('new homework', unit, date, hw)
                                else:
                                    for hw in diary[user][date][unit]:
                                        print('new homework', unit, date, hw)
            prev_diary[user] = diary[user]
            save_diary(prev_diary)
        else:
            print('login err', user)
    except:
        print('err', user)
        print(traceback.format_exc())
save_diary(prev_diary)