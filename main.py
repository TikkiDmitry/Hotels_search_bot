import telebot
from telebot import types
from config import TOKEN, db_url_object
from hotels import request_city
from database import DataBase
from datetime import datetime

bot = telebot.TeleBot(TOKEN)
database = DataBase(db_url_object)

database.create_table()  # Создание таблицы, если её не существует


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, f"Приветствую, {message.from_user.first_name}!\n"
                                           "Я подберу вам лучший отель по вашим критериям\n с сайта Hotels.com\n"
                                           "Для вывода справочной информации используйте /help")


@bot.message_handler(commands=['help'])
def help_handler(message):
    msg = [
        '/lowprice - топ самых дешёвых отелей в городе',
        '/highprice - топ самых дорогих отелей в городе',
        ('/bestdeal -  топ отелей, наиболее подходящих по'
         'цене и расположению от центра'),
        '/history - история поиска отелей',
    ]
    bot.send_message(message.from_user.id, '\n'.join(msg))


@bot.message_handler(commands=['history'])
def history(message):
    his = database.select()
    k = 0
    for i in his:
        if k == 0:
            bot.send_message(message.from_user.id, f'<b>История поиска</b>\n'
                                                   f'Команда: {i[1]}\n'
                                                   f'Отели: {i[3]}\n'
                                                   f'Дата поиска: {i[2]}\n', parse_mode='html')
        else:
            bot.send_message(message.from_user.id, f'Команда: {i[1]}\n'
                                                   f'Отели: {i[3]}\n'
                                                   f'Дата поиска: {i[2]}\n', parse_mode='html')
        k += 1


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def search_low_high_best(message):
    data = []
    if message.text == '/lowprice' or message.text == '/highprice':
        if message.text == '/lowprice':
            data.append('/lowprice')
        elif message.text == '/highprice':
            data.append('/highprice')
        bot.send_message(message.from_user.id, 'Введите на английском языке название города, в котором ищите отель')
        bot.register_next_step_handler(message, get_city, data)
    else:
        if message.text == '/bestdeal':
            data.append('/bestdeal')
            bot.send_message(message.from_user.id, 'Введите на английском языке название города, в котором ищите отель')
            bot.register_next_step_handler(message, get_city_for_best, data)


def get_city_for_best(message, data):
    city = message.text
    data.append(city)
    bot.send_message(message.from_user.id, 'Введите ценовой диапазон через дефис (0000-0000)')
    bot.register_next_step_handler(message, get_cost, data)


def get_cost(message, data):
    cost = message.text
    bot.send_message(message.from_user.id, 'Введите расстояние от центра в метрах')
    bot.register_next_step_handler(message, get_distance, data)


def get_distance(message, data):
    distance = int(message.text)
    bot.send_message(message.from_user.id, 'Введите количество отелей (не более 5)')
    bot.register_next_step_handler(message, get_number_hotels, data)


def get_city(message, data):
    city = message.text
    data.append(city)
    bot.send_message(message.from_user.id, 'Введите количество отелей (не более 5)')
    bot.register_next_step_handler(message, get_number_hotels, data)


def get_number_hotels(message, data):
    number = message.text
    data.append(number)
    get_data_from_site(message, data)

#
# def get_photo_hotels(message):
#     photo = message.text
#     print(photo)
#     if photo.lower() == 'да':
#         bot.send_message(message.from_user.id, 'Сколько фотографий каждого отеля необходимо? (не более 5)')
#         bot.register_next_step_handler(message, get_count_photo)
#     else:
#         get_data_from_site(message)
#
#
# def get_count_photo(message):
#     photo_count = int(message.text)
#     print(photo_count)
#     get_data_from_site(message)


def get_data_from_site(message, data):
    print(data)
    hotels = request_city(data)
    hotels_for_db = ''

    for i in hotels:

        hotels_for_db += i[0] + ', '

        bot.send_message(message.from_user.id, f'<b>Название отеля:</b> {i[0]}\n'
                                               f'<b>Ссылка:</b> {i[1]}', parse_mode='html')
    database.insert(data[0], datetime.today().strftime("%d %b %Y, %A, %H:%M"), hotels_for_db[:-2])


bot.polling(none_stop=True, interval=0)