import telebot
import random
import pyowm

from telebot import types
 
bot = telebot.TeleBot('1315396201:AAEMD9aC_Jo5cyymQDbdovmdiIF3Nwujr6s')
owm = pyowm.OWM('e359e7f9092ae1dabdea2edf5873fc7e') 
mgr = owm.weather_manager()

station_id = 39276

@bot.message_handler(commands=['start'])
def welcome(message):

    bot.send_message(message.chat.id, "Hello")
 
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Узнать дату на сегодня")
    item2 = types.KeyboardButton("Узнать определенную дату")
 
    markup.add(item1, item2)

    bot.send_message(message.chat.id, f"Добро пожаловать, {message.from_user.first_name}!\nЯ - <b>{bot.get_me().first_name}</b>, бот, созданный чтобы показывать тебе погоду любого города.",
        parse_mode='html', reply_markup=markup)
    bot.send_message(message.chat.id, "Введите город:")
    bot.register_next_step_handler(message, weather)


@bot.message_handler(content_types=['text'])
def weather(message):
    answer = message.text

    try:
        observation = mgr.weather_at_place(answer)

        w = observation.weather
        print(w)
        temperature = w.temperature('celsius')['temp']
        bot.send_message(message.chat.id, f"В городе {answer} сейчас температура: {temperature} градуса по цельсию")
    except:
        bot.send_message(message.chat.id, "Извините, данного города не существует. Попробуйте еще раз")


bot.polling(none_stop=True)