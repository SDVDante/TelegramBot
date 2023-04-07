from bs4 import BeautifulSoup
from googletrans import Translator
import telebot
import requests
import random
import time
import datetime
import tweepy



#Telegram
bot = telebot.TeleBot('#')


#Twitter
consumer_key = '#'
consumer_secret = '#'
access_token = '#'
access_secret = '#'


UserID = ''  # ID ПОЛЬЗОВАТЕЛЯ, С КОТОРЫМ ВЕДЁТСЯ ДИАЛОГ (ЗАПИШЕТСЯ ПОСЛЕ КОМАНДЫ /start)
UserFirstName = ''  # ИМЯ ПОЛЬЗОВАТЕЛЯ
UserLastName = ''  # ФАМИЛИЯ ПОЛЬЗОВАТЕЛЯ
UserUsername = ''  # СПЕЦИАЛЬНОЕ ИМЯ ПОЛЬЗОВАТЕЛЯ


old_time = ''  # СТАРОЕ ВРЕМЯ ЗАПРОСА АУГМЕНТАЦИИ
new_time = ''  # НОВОЕ ВРЕМЯ ЗАПРОСА АУГМЕНТАЦИИ


t_list = []  # СПИСОК ТВИТОВ
t_list_dates = []  # СПИСОК ДАТ НАПИСАНИЯ ТВИТОВ
n1 = ''  # СЧЁТЧИК ТВИТОВ - ЛЕВАЯ ГРАНИЦА
n2 = ''  # СЧЁТЧИК ТВИТОВ - ПРАВАЯ ГРАНИЦА


tr_language = ''  # ЯЗЫК ПЕРЕВОДА
tr_text = ''  # ТЕКСТ ДЛЯ ПЕРЕВОДА



@bot.message_handler(commands=['start'])  # ДЕЙСТВИЕ ПО КНОПКЕ "СТАРТ"
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True, input_field_placeholder='Я скажу тебе:')
    keyboard.row('Привет.', 'Хей.')
    keyboard.row('Здравствуй!')
    bot.reply_to(message, f'Моё имя А́дам. Приветствую тебя, {message.from_user.first_name}.', reply_markup=keyboard)
    global UserID, UserFirstName, UserLastName, UserUsername
    UserID = message.chat.id
    UserFirstName = message.from_user.first_name
    UserLastName = message.from_user.last_name
    UserUsername = message.from_user.username


def error(message):  # ДЕЙСТВИЕ ПРИ ЛЮБОЙ ВОЗНИКАЮЩЕЙ ОШИБКЕ/НЕИЗВЕСТНОМ ВВОДЕ
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True, input_field_placeholder='Опси-допси...')
    keyboard.row('🏠 Главное меню')
    otv = ['Пока не знаю, что ты пишешь, но скоро узнаю, честно.\n\nПожалуйста, перейди в главное меню.',
           'Что-то в глаз попало, не понимаю, что ты пишешь, серьёзно.\n\nПожалуйста, перейди в главное меню.',
           'Пока не могу обработать...\n\nПожалуйста, перейди в главное меню.',
           'Я, конечно, хорош, но не настолько, чтобы отвечать '
           'абсолютно на всю ерунду, что ты захочешь мне написать.\n\n'
           'Пожалуйста, перейди в главное меню.']
    choice = random.sample(otv, 1)
    bot.send_message(message.from_user.id, choice, reply_markup=keyboard)


@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.from_user.id, 'Это — главное меню. ⚙\n'
                                           'Здесь описаны все самые основные из доступных на данный момент комманд.\n\nНа выбор:'
                                           '\n\n/facts_about_numbers — рандомный факт о любом введённом тобой числе (eng) 🔢\n\n'
                                           '/horoscope — твой личный гороскоп на сегодня 🌗\n\n'
                                           '/augmentation — получение и установка аугментации дня 🦾\n\n'
                                           '/twitter - просмотр твиттов из профиля SDVDante 🐦\n\n'
                                           '/translator - карманный переводчик 🌍',
                     reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['facts_about_numbers'])
def get_num(message):  # ФАКТЫ О ЧИСЛАХ - ЗАПУСК
    bot.send_message(message.from_user.id, 'На данном этапе доступны только англоязычные версии фактов.\n\n'
                                           'Введи одно или несколько чисел через пробел, чтобы получить интересные факты о них.')
    check = message.text.split(' ')
    if '/menu' in check and len(check) == 1:
        menu(message)
    else:
        bot.register_next_step_handler(message, get_fact)

def get_fact(message):  # ПРОЦЕСС ПОЛУЧЕНИЯ ФАКТОВ О ЧИСЛАХ И ИСКЛЮЧЕНИЯ
    if message.text.lower() in ['/menu', '🏠 главное меню', 'меню', 'menu']:
        menu(message)
    else:
        try:
            numbers = message.text.split(' ')
            for i in numbers:
                api_url = 'http://numbersapi.com/' + i + '/trivia?json=true&default=Кажется, для этого числа ' \
                                                         'не найдено ни одного интересного факта. Жаль.'
                res = requests.get(api_url)
                data = res.json()
                bot.send_message(message.from_user.id, data['text'] + '\n')
            bot.send_message(message.from_user.id, 'А вот и результат.\n'
                                                   'Для перехода в главное меню - введи /menu\n'
                                                   'Для новых фактов - продолжай ввод интересующих чисел.')
            bot.register_next_step_handler(message, get_fact)
        except:
            bot.send_message(message.from_user.id, 'Упс, что-то пошло не так...\n\n'
                                                   'Введи одно или несколько чисел через пробел, чтобы получить интересные факты о них.\n\n'
                                                   'Для перехода в главное меню - введи /menu')
            bot.register_next_step_handler(message, get_fact)


@bot.message_handler(commands=['horoscope'])
def get_smb(message):  # ГОРОСКОП - ЗАПУСК, ВЫВОД КНОПОК СО ЗНАКАМИ НА ВЫБОР
    bot.send_message(message.from_user.id, 'Хочешь узнать гороскоп?\nБез проблем.')
    markup = telebot.types.InlineKeyboardMarkup()
    smb_button1 = telebot.types.InlineKeyboardButton(text='♈ Овен', callback_data='aries')
    smb_button2 = telebot.types.InlineKeyboardButton(text='♉ Телец', callback_data='taurus')
    smb_button3 = telebot.types.InlineKeyboardButton(text='♊ Близнецы', callback_data='gemini')
    smb_button4 = telebot.types.InlineKeyboardButton(text='♋ Рак', callback_data='cancer')
    smb_button5 = telebot.types.InlineKeyboardButton(text='♌ Лев', callback_data='leo')
    smb_button6 = telebot.types.InlineKeyboardButton(text='♍ Дева', callback_data='virgo')
    smb_button7 = telebot.types.InlineKeyboardButton(text='♎ Весы', callback_data='libra')
    smb_button8 = telebot.types.InlineKeyboardButton(text='♏ Скорпион', callback_data='scorpio')
    smb_button9 = telebot.types.InlineKeyboardButton(text='♐ Стрелец', callback_data='sagittarius')
    smb_button10 = telebot.types.InlineKeyboardButton(text='♑ Козерог', callback_data='capricorn')
    smb_button11 = telebot.types.InlineKeyboardButton(text='♒ Водолей', callback_data='aquarius')
    smb_button12 = telebot.types.InlineKeyboardButton(text='♓ Рыбы', callback_data='pisces')
    markup.row(smb_button1, smb_button2, smb_button3)
    markup.row(smb_button4, smb_button5, smb_button6)
    markup.row(smb_button7, smb_button8, smb_button9)
    markup.row(smb_button10, smb_button11, smb_button12)
    bot.send_message(message.chat.id, text='Выбери свой знак зодиака:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('aries', 'taurus', 'gemini', 'cancer', 'leo',
                                                                    'virgo', 'libra', 'scorpio', 'sagittarius',
                                                                    'capricorn', 'aquarius', 'pisces')))

def query_handler(call):  # ПРЕОБРАЗОВАНИЕ И ВЫВОД ГОРОСКОПА
    bot.answer_callback_query(callback_query_id=call.id, text='Сейчас посмотрим...')
    res1 = requests.get('https://horoscopes.rambler.ru/' + call.data)
    res2 = BeautifulSoup(res1.text, 'lxml')
    horoscope = res2.find('div', class_="_1E4Zo _3BLIa").find('p', class_="mtZOt").text
    bot.send_message(call.message.chat.id, horoscope)
    time.sleep(5)
    bot.send_message(call.message.chat.id, 'Что ж, вот и результат.\n'
                                           'Верить ему, или нет - решать только тебе.')
    markup = telebot.types.InlineKeyboardMarkup()
    smb_button1 = telebot.types.InlineKeyboardButton(text='♈ Овен', callback_data='aries')
    smb_button2 = telebot.types.InlineKeyboardButton(text='♉ Телец', callback_data='taurus')
    smb_button3 = telebot.types.InlineKeyboardButton(text='♊ Близнецы', callback_data='gemini')
    smb_button4 = telebot.types.InlineKeyboardButton(text='♋ Рак', callback_data='cancer')
    smb_button5 = telebot.types.InlineKeyboardButton(text='♌ Лев', callback_data='leo')
    smb_button6 = telebot.types.InlineKeyboardButton(text='♍ Дева', callback_data='virgo')
    smb_button7 = telebot.types.InlineKeyboardButton(text='♎ Весы', callback_data='libra')
    smb_button8 = telebot.types.InlineKeyboardButton(text='♏ Скорпион', callback_data='scorpio')
    smb_button9 = telebot.types.InlineKeyboardButton(text='♐ Стрелец', callback_data='sagittarius')
    smb_button10 = telebot.types.InlineKeyboardButton(text='♑ Козерог', callback_data='capricorn')
    smb_button11 = telebot.types.InlineKeyboardButton(text='♒ Водолей', callback_data='aquarius')
    smb_button12 = telebot.types.InlineKeyboardButton(text='♓ Рыбы', callback_data='pisces')
    markup.row(smb_button1, smb_button2, smb_button3)
    markup.row(smb_button4, smb_button5, smb_button6)
    markup.row(smb_button7, smb_button8, smb_button9)
    markup.row(smb_button10, smb_button11, smb_button12)
    bot.send_message(call.message.chat.id, text='Для перехода в главное меню - введи /menu\n'
                                                'Для получения другого гороскопа - выбери нужный знак зодиака:',
                     reply_markup=markup)


@bot.message_handler(commands=['augmentation'])  # АУГМЕНТАЦИЯ - ЗАПУСК, ВЫВОД КНОПОК НА ВЫБОР
def aug_start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    aug_button1 = telebot.types.InlineKeyboardButton(text='Голова', callback_data='head')
    aug_button2 = telebot.types.InlineKeyboardButton(text='Тело', callback_data='body')
    aug_button3 = telebot.types.InlineKeyboardButton(text='Руки', callback_data='arms')
    aug_button4 = telebot.types.InlineKeyboardButton(text='Ноги', callback_data='legs')
    markup.row(aug_button1, aug_button2)
    markup.row(aug_button3, aug_button4)
    bot.send_message(message.chat.id, text='Время выбрать свою аугментацию на сегодня:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('head', 'body', 'arms', 'legs'))) # ПРОВЕРКА ВОЗМОЖНОСТИ АУГМЕНТАЦИИ (ПОВТОРНАЯ УСТАНОВКА ОТКРЫВАЕТСЯ ЧЕРЕЗ СУТКИ)
def aug_check_time(message):
    bot.send_message(message.from_user.id, '⚡ Проверяю возможность аугментирования...')
    time.sleep(2)
    global old_time, new_time
    if old_time == '' and new_time == '':
        aug_get(message)
    else:
        new_time = datetime.datetime.now()
        delta = new_time - old_time  # ПРОШЛО ВРЕМЕНИ С УСТАНОВКИ
        if delta.days < 1:
            #aug_sec_prsh = delta.seconds % (24 * 3600)  # ПРОШЛО ВРЕМЕНИ С УСТАНОВКИ - ЧАСЫ, МИНУТЫ, СЕКУНДЫ
            #aug_hrs_prsh = aug_sec_prsh // 3600
            #aug_sec_prsh = aug_sec_prsh % 3600
            #aug_mins_prsh = aug_sec_prsh // 60
            #aug_sec_prsh = aug_sec_prsh % 60

            delta2 = 86400 - delta.seconds  # ОСТАЛОСЬ ВРЕМЕНИ ДО УСТАНОВКИ

            aug_sec_ost = delta2 % (24 * 3600)  # ОСТАЛОСЬ ВРЕМЕНИ ДО УСТАНОВКИ - ЧАСЫ, МИНУТЫ, СЕКУНДЫ
            aug_hrs_ost = aug_sec_ost // 3600
            aug_sec_ost = aug_sec_ost % 3600
            aug_mins_ost = aug_sec_ost // 60
            aug_sec_ost = aug_sec_ost % 60

            if delta.seconds < 82801:  # ДО ВОССТАНОВЛЕНИЯ ЧАС И БОЛЕЕ - ВЫВОД ЧАСОВ И МИНУТ
                bot.send_message(message.from_user.id, text='Упс...\nТвой организм еще не готов для установки новой аугментации. ⛔\n\n'
                                                'Оставшееся время для восстановления:' + ' ' + str(aug_hrs_ost) + ' ' + 'ч.' + ' ' +
                                                str(aug_mins_ost) + ' ' + 'мин. 🕝' + '\n\nА пока вернёмся в главное меню...')
                time.sleep(2)
                menu(message)
            elif 82801 < delta.seconds < 86341:  # ДО ВОССТАНОВЛЕНИЯ МЕНЕЕ ЧАСА - ВЫВОД МИНУТ
                bot.send_message(message.from_user.id, text='Упс...\nТвой организм еще не готов для установки новой аугментации. ❌\n\n'
                                                'Оставшееся время для восстановления:' + ' ' + str(aug_mins_ost) + ' ' + 'мин. 🕥' +
                                                '\n\nА пока вернёмся в главное меню...')
                time.sleep(2)
                menu(message)
            else:  # ДО ВОССТАНОВЛЕНИЯ МЕНЕЕ МИНУТЫ - ВЫВОД СЕКУНД
                bot.send_message(message.from_user.id,
                                 text='Упс...\nТвой организм еще не готов для установки новой аугментации. ❌\n\n'
                                      'Оставшееся время для восстановления:' + ' ' + str(aug_sec_ost) + ' ' + 'сек. 🕦' +
                                      '\n\nА пока вернёмся в главное меню...')
                time.sleep(2)
                menu(message)
        else:
            aug_get(message)

def aug_get(call):  # ПРОЦЕСС ПОЛУЧЕНИЯ АУГМЕНТАЦИИ И ВЫХОД В МЕНЮ
    global old_time
    old_time = datetime.datetime.now()
    bot.answer_callback_query(callback_query_id=call.id, text='Прогресс не остановить...')
    bot.send_message(call.message.chat.id, 'ВНИМАНИЕ!!!\nВ процессе требуется выполнить несколько простых шагов.')
    time.sleep(3)
    bot.send_message(call.message.chat.id, 'Пожалуйста, сделай глубокий вдох...')
    time.sleep(5)
    bot.send_message(call.message.chat.id, 'Выдох.')
    time.sleep(3)
    bot.send_message(call.message.chat.id, 'Снова вдох...')
    time.sleep(3)
    bot.send_message(call.message.chat.id, 'И выдох.')
    time.sleep(3)
    icon_choice = random.sample(augmentations[call.data], 1)
    txt_choice = random.sample(augmentations_description[str(*icon_choice)], 1)
    bot.send_photo(call.from_user.id, photo=str(*icon_choice), caption=str(*txt_choice))
    time.sleep(8)
    bot.send_message(call.from_user.id, 'Поздравляю с успешной установкой аугментации! '
                                        'Напомню: один день - одна модификация, так как организму требуется некоторое время '
                                        'на восстановление. 🔄\n\nПо этой причине осуществим переход сразу в главное меню...')
    time.sleep(5)
    menu(call)

augmentations = {'head': ['https://imgur.com/hrNH40M', 'https://imgur.com/INVCoa0'], # ССЫЛКИ НА КАРТИНКИ К АУГМЕНТАЦИЯМ
                 'body': ['https://imgur.com/S3oT71e', 'https://imgur.com/mL77z5E'],
                 'arms': ['https://imgur.com/fprg0FX', 'https://imgur.com/JdzD7Jj'],
                 'legs': ['https://imgur.com/fM0RK3k', 'https://imgur.com/l7lmRYQ']}

augmentations_description = {'https://imgur.com/hrNH40M': ['✅ Готово!\n\nНе знаю, что было с ним вчера, или, что будет завтра, но ' # голова-зренение/бдительность
                                                           'сегодня твоё зрение будет чуть острее, чем обычно. '
                                                           'Особенно полезно при работе за компьютером. 👁',
                                                           '✅ Сделано!\n\nЗрение - важная штука. На весь сегодняшний день, '
                                                           'благодаря установленной аугментации, твоё зрение будет на '
                                                           'несколько пунктов лучше, чем обычно. А теперь - за дело. 👁'],
                             'https://imgur.com/INVCoa0': ['✅ Готово!\n\nХороший слух крайне важен при выполнении самых ' # голова-слух
                                                           'разных задач. Благодаря установленной аугментации, сегодня '
                                                           'у тебя точно не будет с ним никаких проблем. 🦻',
                                                           '✅ Аугментация установлена!\n\nИзмененная кохлеарная аугментация "Ртуть" - как бы страшно '
                                                           'это не звучало, но твоя чуткость и скорость реакции на '
                                                           'сегодня повышены.\nНикаких неожиданностей. 🦻'],
                             'https://imgur.com/S3oT71e': ['✅ Процесс установки завершен!\n\nАугментация возвратного дыхания, придающая ' # тело-укрепление-легких
                                                           'организму дополнительное количество кислорода, позволит сохранять '
                                                           'бодрость и избегать усталости гораздо дольше, чем обычно. 🫁',
                                                           '✅ Установка выполнена!\n\nВыворачивает от самых незначительных неприятных '
                                                           'запахов? Сегодня с этим будет полегче - химических фильтр поможет переносить '
                                                           'подобные условия с гордо поднятой головой.\nДа здравствует чистый воздух! 🫁'],
                             'https://imgur.com/mL77z5E': ['✅ Сделано!\n\nКрайне важно держать своё тело в форме. Данная аугментация поможет тебе ' # тело-укрепление-брони
                                                           'с этим, хоть и всего на день - кратковременное укрепление мускулатуры тела. Как раз '
                                                           'то, что нужно для выполнения повседневных (и не только) подвигов. 🛡',
                                                           '✅ Готово!\n\nПолучение урона и травм - процесс не из приятных. Даже мелкие царапины могут доставлять '
                                                           'немалый дискомфорт, поэтому на сегодня твой порог допустимого урона немного повышен. 🛡'],
                             'https://imgur.com/fprg0FX': ['✅ Установка завершена!\n\nРуки - хорошо. Крепкие руки - вообще отлично. ' # руки-укрепление-рук 
                                                           'В течение всего дня твои руки будут выдерживать гораздо большую нагрузку, чем обычно. '
                                                           'Возможно, пришло время завершить давно отложенные дела? 💪',
                                                           '✅ Установка выполнена!\n\nМелкая моторика и точные движения рук - навыки, важные не только '
                                                           'для хирургов. Сегодня у тебя с этим проблем точно не будет. Действуй. 💪'],
                             'https://imgur.com/JdzD7Jj': ['✅ Аугментация установлена!\n\nМиомерные модули, подвергнутые дополнительной оптимизации, способны заметно ' # руки-грузоподъемность
                                                           'увеличить физическую силу. Один из самых заметных плюсов - перемещение тяжёлых предметов сегодня '
                                                           'будет даваться несколько легче, чем обычно. 🦾',
                                                           '✅ Процесс установки завершён!\n\nПовышенная грузоподъёмность может быть полезна даже при выполнении самых '
                                                           'базовых домашних дел. На сегодня уровень твоей силы повышен. Хотя, таскать сверх меры, разумеется, не стоит. 🦾'],
                             'https://imgur.com/fM0RK3k': ['✅ Установка аугментации завершена!\n\nУкрепление мускулатуры ног даёт значительное преимущество при ' # ноги-укрепление-ног
                                                           'выполнении самых различных дел - от готовки завтрака до спасения мира. Как итог на сегодня: мышечные '
                                                           'ткани ног были заметно усилены. 🦵',
                                                           '✅ Сделано!\n\nБлагодаря данной аугментации мышечные ткани ног переживают заметное укрепление, хоть и '
                                                           'всего на один день. Повышенная выносливость ног поможет при выполнении любых поставленных задач.\nВремя действовать! 🦵'],
                             'https://imgur.com/l7lmRYQ': ['✅ Установка выполнена!\n\nДаже небольшое повышение скорости бега, и передвижения в целом, может оказаться крайне полезным ' # ноги-ускорение
                                                           'в самых чрезвычайных ситуациях. Только не стоит забывать, что данное улучшение будет активно лишь в течение одного дня. 🦿',
                                                           '✅ Готово!\n\nУвеличение скорости передвижения и бега, которое будет активно в течение всего дня. Хорошее дополнение, особенно, '
                                                           'если на день намечено много срочных дел. 🦿']
                             }


@bot.message_handler(commands=['twitter'])
def twitter_start(message):  # ТВИТТЕР - ЗАПУСК И ВЫБОР ОТСЕИВАНИЯ РЕТВИТТОВ
    markup = telebot.types.InlineKeyboardMarkup()
    ret_button1 = telebot.types.InlineKeyboardButton(text='Оставить ретвиты', callback_data='save_ret')
    ret_button2 = telebot.types.InlineKeyboardButton(text='Убрать ретвиты', callback_data='del_ret')
    markup.row(ret_button1, ret_button2)
    bot.send_message(message.chat.id, text='Что ж, посмотрим, что там нового.\nЛучше с ретвитами, или без?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('save_ret','del_ret'))) #  ПОЛУЧЕНИЕ ТВИТОВ И ЗАНЕСЕНИЕ ИХ В СПИСОК
def tweets_get(call):
    from datetime import datetime, date, time, timedelta
    global t_list, t_list_dates
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    if call.data == 'save_ret':
        t_list = []  # СПИСОК ТВИТОВ
        t_list_dates = []  # СПИСОК ДАТ НАПИСАНИЯ ТВИТОВ
        my_tweets = api.user_timeline(include_rts=True, count=200)  # ТВИТЫ С РЕТВИТАМИ (ЗНАЧЕНИЕ В 200 - МАКСИМУМ ПРИ ОТОБРАЖЕНИИ)
        for i in my_tweets:
            if i.text[0:2] == 'RT':
                i.text = 'Ретвит пользователя' + i.text[2:]
                t_list += [i.text]
                year = str(i.created_at)[0:4]  # ПЕРЕВОД с UTC НА МОСКОВСКОЕ ВРЕМЯ (+3 ЧАСА) И ВЫВОД В НУЖНОМ ФОРМАТЕ: ДЕНЬ, МЕСЯЦ, ГОД, ЧАСЫ, МИНУТЫ
                month = str(i.created_at)[5:7]
                day = str(i.created_at)[8:10]
                hour = str(i.created_at)[11:13]
                min = str(i.created_at)[14:16]
                perevod_utc = datetime(int(year), int(month), int(day), int(hour), int(min))
                perevod_utc = perevod_utc + timedelta(hours=3)  #  ИДЁТ ПЕРЕВОД - ПРИБАВЛЯЕТСЯ ТРИ ЧАСА
                t_list_dates += [str(perevod_utc)[8:10] + '.' + str(perevod_utc)[5:7] + '.' + str(perevod_utc)[0:4] + ' ' + str(perevod_utc)[11:16]]
            else:
                t_list += [i.text]
                year = str(i.created_at)[0:4]  # ПЕРЕВОД с UTC НА МОСКОВСКОЕ ВРЕМЯ (+3 ЧАСА) И ВЫВОД В НУЖНОМ ФОРМАТЕ: ДЕНЬ, МЕСЯЦ, ГОД, ЧАСЫ, МИНУТЫ
                month = str(i.created_at)[5:7]
                day = str(i.created_at)[8:10]
                hour = str(i.created_at)[11:13]
                min = str(i.created_at)[14:16]
                perevod_utc = datetime(int(year), int(month), int(day), int(hour), int(min))
                perevod_utc = perevod_utc + timedelta(hours=3)
                t_list_dates += [str(perevod_utc)[8:10] + '.' + str(perevod_utc)[5:7] + '.' + str(perevod_utc)[0:4] + ' ' + str(perevod_utc)[11:16]]
    elif call.data == 'del_ret':
        t_list = []  # СПИСОК ТВИТОВ
        t_list_dates = []  # СПИСОК ДАТ НАПИСАНИЯ ТВИТОВ
        my_tweets = api.user_timeline(include_rts=False, count=200)  # ТВИТЫ БЕЗ РЕТВИТОВ (ЗНАЧЕНИЕ В 200 - МАКСИМУМ ПРИ ОТОБРАЖЕНИИ)
        for i in my_tweets:
            t_list += [i.text]
            year = str(i.created_at)[0:4]  # ПЕРЕВОД с UTC НА МОСКОВСКОЕ ВРЕМЯ (+3 ЧАСА) И ВЫВОД В НУЖНОМ ФОРМАТЕ: ДЕНЬ, МЕСЯЦ, ГОД, ЧАСЫ, МИНУТЫ
            month = str(i.created_at)[5:7]
            day = str(i.created_at)[8:10]
            hour = str(i.created_at)[11:13]
            min = str(i.created_at)[14:16]
            perevod_utc = datetime(int(year), int(month), int(day), int(hour), int(min))
            perevod_utc = perevod_utc + timedelta(hours=3)
            t_list_dates += [str(perevod_utc)[8:10] + '.' + str(perevod_utc)[5:7] + '.' + str(perevod_utc)[0:4] + ' ' + str(perevod_utc)[11:16]]
    global n1, n2
    n1 = 0
    n2 = 3
    tweets_show(call)

def tweets_show(message):  # ВЫВОД ТВИТОВ И КНОПОК ПРОДОЛЖЕНИЯ
    newtwt_icons = ['🆕', '⚡', '💥', '🔥']
    newtwt_icon = random.sample(newtwt_icons, 1)
    global n1, n2, t_list, t_list_dates
    try:
        for z in range(n1, n2):
            if z == 0:  # ВЫВОД ПЕРВОГО ТВИТА С ОСОБОЙ ИКОНКОЙ НОВИНКИ
                bot.send_message(message.from_user.id, str(*newtwt_icon) + ' ' + t_list_dates[z] + '\n' + '«' + t_list[z] + '»')
            else:
                if z == len(t_list) - 1:  # ОГРАНИЧИТЕЛЬ ВЫВОДА (И ВЫВОД ПОСЛЕДНЕГО ТВИТА)
                    markup = telebot.types.InlineKeyboardMarkup()
                    twt_button1 = telebot.types.InlineKeyboardButton(text='Предыдущие твиты', callback_data='prvstwts')
                    twt_button2 = telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='mainmenu')
                    markup.row(twt_button1, twt_button2)
                    bot.send_message(message.from_user.id, '🗓' + ' ' + t_list_dates[z] + '\n' + '«' + t_list[z] + '»')
                    bot.send_message(message.from_user.id,
                                     text='Извини, соваться дальше я не стану. Дело такое - начнёшь - не остановишься.\n\n'
                                          'Может, вернёмся в главное меню?', reply_markup=markup)
                    break
                elif z == n2 - 1:  # ВЫВОД ПОСЛЕДНЕГО ТВИТА В ЦИКЛЕ ИЗ ТРЁХ
                    if n1 == 0:  # ПОСЛЕДНИЙ ТВИТ В ЦИКЛЕ И ЭТО САМЫЙ ПЕРВЫЙ ЦИКЛ
                        markup = telebot.types.InlineKeyboardMarkup()
                        twt_button1 = telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='mainmenu')
                        twt_button2 = telebot.types.InlineKeyboardButton(text='Ещё несколько твитов', callback_data='nexttwts')
                        markup.row(twt_button1, twt_button2)
                        bot.send_message(message.from_user.id, '🗓' + ' ' + t_list_dates[z] + '\n' + '«' + t_list[z] + '»', reply_markup=markup)
                    else:  # ПОСЛЕДНИЙ ТВИТ В ЦИКЛЕ
                        markup = telebot.types.InlineKeyboardMarkup()
                        twt_button1 = telebot.types.InlineKeyboardButton(text='Предыдущие твиты', callback_data='prvstwts')
                        twt_button2 = telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='mainmenu')
                        twt_button3 = telebot.types.InlineKeyboardButton(text='Следующие твиты', callback_data='nexttwts')
                        markup.row(twt_button1, twt_button2, twt_button3)
                        bot.send_message(message.from_user.id, '🗓' + ' ' + t_list_dates[z] + '\n' + '«' + t_list[z] + '»', reply_markup=markup)
                else:  # ВЫВОД ТВИТА В ЦИКЛЕ
                    bot.send_message(message.from_user.id, '🗓' + ' ' + t_list_dates[z] + '\n' + '«' + t_list[z] + '»')
    except Exception:
        bot.answer_callback_query(callback_query_id=message.id, text='А больше потыкать некуда?')
        menu(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('prvstwts', 'mainmenu', 'nexttwts'))) #  КНОПКИ ПЕРЕХОДА К ПРЕДЫДУЩИМ/СЛЕДУЮЩИМ ТВИТАМ ИЛИ ГЛАВНОМУ МЕНЮ
def tweets_choice(call):
    global n1, n2, t_list
    if call.data == 'prvstwts':
        n1 -= 3
        n2 -= 3
        if n1 >= len(t_list):  # ОГРАНИЧИТЕЛЬ ПЕРЕХОДА НА ЧИСЛО, ПРЕВЫШАЮЩЕЕ КОЛИЧЕСТВО ДОСТУПНЫХ ТВИТОВ В СПИСКЕ
            bot.answer_callback_query(callback_query_id=call.id, text='Шалость не удалась.')
            menu(call)
        elif n1 < 0:  # ОГРАНИЧИТЕЛЬ ПЕРЕХОДА НА ОТРИЦАТЕЛЬНОЕ ЧИСЛО
            n1 = 0
            n2 = 3
            tweets_show(call)
        else:
            tweets_show(call)
    elif call.data == 'nexttwts':
        n1 += 3
        n2 += 3
        if n1 >= len(t_list):  # ОГРАНИЧИТЕЛЬ ПЕРЕХОДА НА ЧИСЛО, ПРЕВЫШАЮЩЕЕ КОЛИЧЕСТВО ДОСТУПНЫХ ТВИТОВ В СПИСКЕ
            bot.answer_callback_query(callback_query_id=call.id, text='Шалость не удалась.')
            menu(call)
        else:
            tweets_show(call)
    elif call.data == 'mainmenu':
        menu(call)


tr_greet = ['🌐 Замечу, что исходный язык того, что ты напишешь, я определю самостоятельно.\nИтак, что переводим?', #  ПЕРЕВОДЧИК - ПРИВЕТСТВИЯ
            '🌐 Замечу, что исходный язык того, что ты напишешь, я смогу определить самостоятельно.\nЧто требуется перевести?',
            '🌐 Замечу, что исходный язык того, что ты напишешь, я определю самостоятельно.\nЧто переводим?']

@bot.message_handler(commands=['translator'])
def tr_start(message):  #  ЗАПУСК ПЕРЕВОДЧИКА С РАНДОМНЫМ ВЫБОРОМ ПРИВЕТСТВИЯ
    tr_gr = random.sample(tr_greet, 1)
    bot.send_message(message.chat.id, text=tr_gr)
    bot.register_next_step_handler(message, tr_lang)

def tr_lang(message):   #  ВЫВОД КНОПОК ДЛЯ ВЫБОРА ЯЗЫКА ПЕРЕВОДА
    global tr_text
    tr_text = message.text
    markup = telebot.types.InlineKeyboardMarkup()
    tr_button1 = telebot.types.InlineKeyboardButton(text='🇬🇧 Английский', callback_data='en')
    tr_button2 = telebot.types.InlineKeyboardButton(text='🇩🇪 Немецкий', callback_data='de')
    tr_button3 = telebot.types.InlineKeyboardButton(text='🇫🇷 Французский', callback_data='fr')
    tr_button4 = telebot.types.InlineKeyboardButton(text='🇮🇹 Итальянский', callback_data='it')
    tr_button5 = telebot.types.InlineKeyboardButton(text='🇪🇸 Испанский', callback_data='es')
    tr_button6 = telebot.types.InlineKeyboardButton(text='🇷🇺 Русский', callback_data='ru')
    tr_button7 = telebot.types.InlineKeyboardButton(text='🇯🇵 Японский', callback_data='ja')
    tr_button8 = telebot.types.InlineKeyboardButton(text='🇨🇳 Китайский (упрощённый)', callback_data='zh-cn')
    markup.row(tr_button1, tr_button2)
    markup.row(tr_button3, tr_button4)
    markup.row(tr_button5, tr_button6)
    markup.row(tr_button7, tr_button8)
    bot.send_message(message.chat.id, text='Принято. На какой язык переводим?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('en','de','fr','it','es','ru','ja','zh-cn')))  #  ЗАПУСК ПЕРЕВОДА И ВЫВОД РЕЗУЛЬТАТА
def tr_res(call):
    global tr_language, tr_text
    tr_language = call.data
    translator = Translator()
    translation = translator.translate(dest=tr_language, text=tr_text)
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True, input_field_placeholder='Что-нибудь ещё?')
    keyboard.row('Далее ➡')
    keyboard.row('🏠 Главное меню')
    bot.send_message(call.from_user.id, translation.text, reply_markup=keyboard)
    bot.send_message(call.from_user.id, 'Если требуется перевести что-нибудь ещё - нажми на кнопку «Далее».\n'
                                        'Если необходимо вернуться в меню - ты знаешь, что делать.')



@bot.message_handler(commands=['version'])
def ver(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True, input_field_placeholder='−−−••• −•−−•−')
    keyboard.row('🏠 Главное меню')
    bot.send_message(message.from_user.id,
                                        '            👁‍🗨 Ádam — Версия 1.0 👁‍🗨\n\n'
                                           '              Последние изменения:\n\n'
                                           '⭐ Добавлен основной сборник команд и их составляющих:\n/facts_about_numbers — факты о числах (версия на английском),\n'
                                           '/horoscope — гороскопы,\n/augmentation — выбор аугментаций,\n/twitter — твиттер SDVDante,\n'
                                           '/translator — карманный переводчик;\n\n'
                                           '⭐ Добавлены вспомогательные команды:\n/menu - главное меню,\n'
                                           '/version - информация о последней версии бота;\n\n'
                                           '⭐ Добавлены фоновые и секретные команды;\n\n'
                                           '⭐ Добавлены ответные реплики и многое другое.\n\n', reply_markup=keyboard)



@bot.message_handler(content_types=['text']) # СЛУЧАЙНЫЕ ТЕКСТОВЫЕ КОМАНДЫ ДЛЯ ДАЛЬНЕЙШЕГО ДОПОЛНЕНИЯ
def get_text_messages(message):
    z = message.text = message.text.lower()
    b = bot.send_message
    if z == 'а':
        error(message)
    elif z == '🏠 главное меню':
        menu(message)
    elif z == 'далее ➡':
        tr_start(message)
    elif z in ['привет', 'привет.', 'хей.', 'хай', 'хей', 'здарова', 'здравствуй!']:
        menu(message)
    elif z in ['Узнал?']:
        b(message.from_user.id, 'Согласен.')
    else:
        error(message)



bot.polling(none_stop=True)
# print(UserID, UserFirstName, UserLastName, UserUsername)