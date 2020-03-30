import requests, telebot, time, os, traceback

os.chdir('EschoolBot')

bot = telebot.TeleBot(open('bothash.txt', 'r').readline().rstrip())

cur = {int(i.rstrip().split()[0]): int(i.rstrip().split()[1]) for i in open('cur.txt', 'r')}

text = 'Добавил в бота функцию просмотра домашнего задания на выбранный день по команде /get\\_homework. В будущем может быть добавлю оповещения о новых домашних заданиях.\n\n*Для тех, кого не устраивают лаги бота при некоторых командах:*\nИз-за того как устроен дневник, для того чтобы получить инфу о дз или оценках нужно посылать по несколько запросов, на которые Eschool отвечает очень медленно, из-за чего время отклика может быть долгим. *Это проблемы не бота, а именно серверов дневника*'
for id in cur:
    try:
        print(bot.send_message(id, text, parse_mode="Markdown"))
        time.sleep(0.3)
    except:
        print('err', id)
