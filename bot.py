
# # To'liq dastur
import requests
import telebot
from telebot import types

bot = telebot.TeleBot("7669799368:AAEwga1aMDG0xYOFMlyiwOAanzxxafB7YCU")

def weather_by_coordinates(lat, lon):
    API_KEY = "9bbd3bcabc8513c29ce6069e29ac4e22"
    url = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&lang=ru")
    data = url.json()
    return data


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_location = types.KeyboardButton(text="Joylashuvni yuborish", request_location=True)
    keyboard.add(button_location)
    bot.send_message(message.chat.id, "Iltimos, joylashuvingizni yuboring:", reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    if message.location is not None:
        lat = message.location.latitude
        lon = message.location.longitude
        bot.send_message(message.chat.id, f"Sizning joylashuvingiz: Latitude: {lat}, Longitude: {lon}")

        data = weather_by_coordinates(lat, lon)

        if data:
            status = data['weather'][0]["description"]
            temp = data["main"]["temp"]
            celsius = round(temp - 273.15, 2)
            city = data["name"]
            response = f"Ob-havo {city} uchun: {celsius}°C, {status}"
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "Ob-havo ma'lumotini olishda xatolik!")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Iltimos, joylashuvingizni yuboring yoki boshqa xabar yuboring.")

bot.infinity_polling()