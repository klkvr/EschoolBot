import requests, telebot, time, os, traceback

os.chdir('EschoolBot')

bot = telebot.TeleBot(open('bothash.txt', 'r').readline().rstrip())

cur = {int(i.rstrip().split()[0]): int(i.rstrip().split()[1]) for i in open('cur.txt', 'r')}

text = 'Tеперь бот будет оповещать вас о новых выложенных домашних заданиях. Для тех, кому эта функция будет не нужна скоро сделаю команду для ее отключения.\nТакже код бота теперб доступен на GitHub: https://github.com/klkvr/EschoolBot'
for id in cur:
    try:
        print(bot.send_message(id, text, parse_mode="Markdown"))
        time.sleep(0.3)
    except:
        print('err', id)
