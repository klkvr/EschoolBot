import requests, telebot, time, os, traceback

os.chdir('EschoolBot')

bot = telebot.TeleBot(open('bothash.txt', 'r').readline().rstrip())

cur = {int(i.rstrip().split()[0]): int(i.rstrip().split()[1]) for i in open('cur.txt', 'r')}

text = 'Дневник сейчас очень плохо справляется с нагрузкой из-за огромного количества файлов с дз, передаваемых через диалоги с учителями, и из-за этого он ограничил количество запросов с одного IP-адреса. Так что на данный момент уведомления ни о дз ни о оценках приходить не будут'
for id in cur:
    try:
        print(bot.send_message(id, text, parse_mode="Markdown"))
        time.sleep(0.3)
    except:
        print('err', id)
