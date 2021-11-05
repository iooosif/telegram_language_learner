import random

import telebot

from info import token as tkn

bot = telebot.TeleBot(tkn)
# соединение бота с токеном
correct = 0
mistakes = 0
c = 0
k = 0
list_rus = []
list_czech = []
set_errors = set()


# списки русских слов и чешских ,счетчик ошибок, переменная счетчик для
# прогона по спискам, переменная для определенния какой это по счету кругу и список слов с ошибкой

def update_lists():
    global list_rus, list_czech

    with open('rus.txt', 'r') as rus:
        with open('czech.txt', 'r') as czech:
            list_rus = [i for i in rus]
            list_czech = [j for j in czech]
            print('открылись файлы')

            mix()
            # добавляем данные из файлов в листы


# синхронная перемешка списков
def mix():
    global list_rus, list_czech
    mixture_list = list(zip(list_rus, list_czech))
    random.shuffle(mixture_list)
    list_rus, list_czech = zip(*mixture_list)
    list_rus, list_czech = list(list_rus), list(list_czech)
    print(type(list_rus))


@bot.message_handler(commands=['commands'])
def wright_commands(message):
    bot.send_message(message.from_user.id,
                     'список команд этого бота:\n /start - обновить игру и начать сначала \n /break - закончить игру \n'
                     '/result - выводит результаты \n /commands - выводит список команд')


# пишет результат
@bot.message_handler(commands=['result'])
def results(message):
    try:
        bot.send_message(message.from_user.id,
                         'вы набрали {0} правильных и {1} неправильных'.format(correct, mistakes))
        if mistakes != 0:
            bot.send_message(message.from_user.id, 'вы допустили ошибки в этих словах {0}'.format(set_errors))
        bot.send_message(message.from_user.id, list_rus[c])
    except:
        start_work(message)


@bot.message_handler(commands=['start', 'break'])
# обработчик команды старт и брейк
def start_work(message):
    global k, c, correct, mistakes
    correct = 0
    mistakes = 0
    c = 0
    k = 0
    set_errors.clear()
    update_lists()
    # обновляем все переменные до первоначального значения
    bot.send_message(message.from_user.id, 'все началось с начала')


# обработчик текста
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global k, c, correct, mistakes
    try:
        # проверяем на превышение счетчика длины словоря
        if k == 0:
            # если первое сообщение(или после команд брейк и старт)
            update_lists()
            k += 1
            bot.send_message(message.from_user.id, list_rus[c])
            print('начало просмотра ')

        else:

            if (message.text == list_czech[c][:-1]) or (message.text == list_czech[c]):

                bot.send_message(message.from_user.id, 'правильно')

                c += 1
                correct += 1
                # если ответили правильно, то начинаем все как было
                bot.send_message(message.from_user.id, list_rus[c])
            else:
                bot.send_message(message.from_user.id, 'не правильно')
                bot.send_message(message.from_user.id, list_czech[c])
                list_rus.append(list_rus[c])
                list_czech.append(list_czech[c])
                set_errors.add("{0} : {1}".format(list_rus[c].replace('\n', ''), list_czech[c].replace('\n', '')))
                print('добавление новых вариантов ')

                c += 1
                mistakes += 1
                bot.send_message(message.from_user.id, list_rus[c])
                # если не правильно ответили, то слова вновь добавляются в конец списков
                # и добавляется в список ошибок
    except:
        # если счетчик превысил длинну списка, то выводим результаты
        if correct == 3:
            results(message)


# бесконечная работа бота
bot.polling(none_stop=True, interval=0)

"""
bot.delete_webhook()
bot.set_webhook('https://test.com/' + tkn)"""
