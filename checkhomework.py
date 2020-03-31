import requests, time, codecs, traceback, telebot, os


def save_diary(diary):
    f = codecs.open('prevdiary.txt', 'w')
    print(diary, file=f)
    f.close()

os.chdir('EschoolBot')
bot = telebot.TeleBot(open('bothash.txt', 'r').readline().rstrip())

week = {'Mon': 'Понедельник', 'Tue': 'Вторник', 'Wed': 'Среду', 'Thu': 'Четверг', 'Fri': 'Пятницу', 'Sat': 'Субботу', 'Sun': 'Воскресенье'}
month = {'Mar': 'Марта', 'Apr': 'Апреля', 'May': 'Мая', 'Sep': 'Сентября', 'Nov': 'Ноября', 'Dec': 'Декабря', 'Jan': 'Января', 'Feb': 'Февраля'}
hwoff = [int(i.rstrip()) for i in open('hwoff.txt', 'r')]
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
                                            if user not in hwoff:
                                                ti = time.ctime(date).split()[:3]
                                                t = week[ti[0]] + ', ' + ti[2] + ' ' + month[ti[1]]
                                                msg = 'Новое домашнее задание по предмету *' + unit + '* на ' + t + ':\n' + hw['text'] + '\n\n/off_homework - отключить уведомления о домашних заданиях'
                                                bot.send_message(user, msg, parse_mode="Markdown")
                                                for file in hw['file']:
                                                    id = file['id']
                                                    name = f['fileName']
                                                    f = open(name, 'wb')
                                                    f.write(s.get('https://app.eschool.center/ec-server/files/' + str(id), cookies=s.cookies).content)
                                                    f.close()
                                                    bot.send_document(user, open(name, 'rb'))
                                                    os.remove(name)
                                            print('new homework', unit, date, hw)
                                else:
                                    for hw in diary[user][date][unit]:
                                        if user not in hwoff:
                                            ti = time.ctime(date).split()[:3]
                                            t = week[ti[0]] + ', ' + ti[2] + ' ' + month[ti[1]]
                                            msg = 'Новое домашнее задание по предмету *' + unit + '* на ' + t + ':\n' + hw[
                                                'text'] + '\n\n/off_homework - отключить уведомления о домашних заданиях'
                                            bot.send_message(user, msg, parse_mode="Markdown")
                                            for file in hw['file']:
                                                id = file['id']
                                                name = f['fileName']
                                                f = open(name, 'wb')
                                                f.write(s.get('https://app.eschool.center/ec-server/files/' + str(id),
                                                              cookies=s.cookies).content)
                                                f.close()
                                                bot.send_document(user, open(name, 'rb'))
                                                os.remove(name)
                                        print('new homework', unit, date, hw)
            prev_diary[user] = diary[user]
            save_diary(prev_diary)
        else:
            print('login err', user)
    except:
        print('err', user)
        bot.send_message('@eschool239boterrors', traceback.format_exc())
save_diary(prev_diary)
