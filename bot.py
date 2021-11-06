import random
import tg_analytic

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
base_len_list = 0

# списки русских слов и чешских ,счетчик ошибок, переменная счетчик для
# прогона по спискам, переменная для определенния какой это по счету кругу и список слов с ошибкой

def update_lists(message):
    global list_rus, list_czech, base_len_list

    with open('dicts/rus_' + message + '.txt', 'r') as rus:
        with open('dicts/czech_' + message + '.txt', 'r') as czech:
            list_rus = [i for i in rus]
            list_czech = [j for j in czech]
            print('открылись файлы')
            base_len_list = len(list_rus)
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



# описание бота
@bot.message_handler(commands=['description'])
def description(message):
    tg_analytic.statistics(message.chat.id)
    bot.send_message(message.from_user.id, 'Этот бот должен помочь вам в изучении'
                                           'чешского языка,\n просто ежедневно проходите '
                                           'тест по интересующей вас лексике.\n'
                                           'Желаем вам приятного изучения языка!')


# выводит список команд
@bot.message_handler(commands=['commands'])
def wright_commands(message):
    tg_analytic.statistics(message.chat.id)
    bot.send_message(message.from_user.id,
                     'список команд этого бота:\n /restart - обновить игру и '
                     'начать сначала \n /break - закончить игру \n'
                     '/result - выводит результаты \n /commands - выводит список команд\n'
                     '/description - выводит краткое описание бота')
    if c != 0:
        bot.send_message(message.from_user.id, list_rus[c])


# пишет результат
@bot.message_handler(commands=['result'])
def results(message):
    tg_analytic.statistics(message.chat.id)
    try:
        bot.send_message(message.from_user.id,
                         'вы набрали {0} правильных и {1} неправильных'.format(correct, mistakes))
        if mistakes != 0:
            bot.send_message(message.from_user.id, 'вы допустили ошибки в этих словах {0}'.format(set_errors))

    except:
        start_work(message)
    bot.send_message(message.from_user.id, 'чтобы начать сначала, введите команду /restart')


@bot.message_handler(commands=['restart', 'break'])
# обработчик команды старт и брейк
def start_work(message):
    global k, c, correct, mistakes
    tg_analytic.statistics(message.chat.id)
    correct = 0
    mistakes = 0
    c = 0
    k = 0
    set_errors.clear()

    # обновляем все переменные до первоначального значения
    bot.send_message(message.from_user.id, 'все началось с начала')


# обработчик текста
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global k, c, correct, mistakes
    tg_analytic.statistics(message.chat.id)
    try:
        # проверяем на превышение счетчика длины словоря
        if k == 0:
            k += 1
            bot.send_message(message.from_user.id,
                             'выберите словарь по которому будете заниматься (family, days, contact, thanks)')
        # выбираем словарь
        elif k == 1:
            # если первое сообщение(или после команд брейк и старт)
            try:
                update_lists(message.text.lower())
            except:
                bot.send_message(message.from_user.id,
                                 'такого словаря нет, отправьте любой символ и попробуйте еще раз')
                k = -1

            k += 1
            bot.send_message(message.from_user.id, list_rus[c])
            print('начало просмотра ')

        else:

            if (message.text.lower() == list_czech[c][:-1].lower()) or (message.text.lower() == list_czech[c].lower()):

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
        if correct == base_len_list:
            results(message)


# бесконечная работа бота
bot.polling(none_stop=True, interval=0)

"""
bot.delete_webhook()
bot.set_webhook('https://test.com/' + tkn)"""
# беспрерывной доступ к телеграм апи
