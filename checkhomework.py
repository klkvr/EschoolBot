
import requests, time, codecs, traceback

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
user_id = 410821501
diary = {}
for user in users_data:
    try:
        s = requests.Session()
        l = s.post('https://app.eschool.center/ec-server/login', data=users_data[user]['login_data'])
        timee = (int(time.time()) // 86400) * 86400 - 86400 * 14
        getdiary = requests.get('https://app.eschool.center/ec-server/student/diary?userId=' + str(users_data[user]['id']) + '&d1=' + str(timee * 1000) + '&d2=' + str((timee + 86400 * 14) * 1000), cookies=s.cookies).json()['lesson']
        diary[user] = {}
        for i in getdiary:
            date = i['date'] // 1000
            unit = i['unit']['name']
            if date not in diary:
                diary[user][date] = {}
            if unit not in diary[user][date]:
                diary[user][date][unit] = []
            for j in i['part']:
                diary[user][date][unit].extend([{'text': elem['text'], 'file': elem['file']} for elem in j['variant']])
    except:
        print('err', user)
        print(traceback.format_exc())
f = codecs.open('prevhomework.txt', 'w')
print(diary, file=f)
f.close()