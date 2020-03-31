
import requests, time

users_data = {int(i.rstrip().split()[0]): {'login_data':
                                               {'username': i.rstrip().split()[1:-2],
                                                'password': i.rstrip().split()[-2]},
                                           'id': int(i.rstrip().split()[-1])} for i in open('pal.txt', 'r')}

user_id = 410821501
s = requests.Session()
l = s.post('https://app.eschool.center/ec-server/login', data=users_data[user_id]['login_data'])
timee = int(time.time()) - 86400 * 30
getdiary = requests.get('https://app.eschool.center/ec-server/student/diary?userId=' + str(users_data[user_id]['id']) + '&d1=' + str(timee * 1000), cookies=s.cookies).json()['lesson']
diary = {}
for i in getdiary:
    date = i['date'] // 1000
    unit = i['unit']['name']
    if date not in diary:
        diary[date] = {}
    if unit not in diary[date]:
        diary[date][unit] = []
    for j in i['part']:
        diary[date][unit].extend([{'text': elem['text'], 'file': elem['file']} for elem in j['variant']])
for date in diary:
    print(str(date) + ':')
    for unit in diary[date]:
        print('    ' + unit + ':')
        for dz in diary[date][unit]:
            print('        ', dz)