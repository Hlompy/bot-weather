import datetime as dt
import logging
import os

import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s, %(name)s, %(levelname)s, %(message)s',
    level=logging.DEBUG,
    filename='main.log',
    filemode='w',
    encoding='UTF-8'
)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')

WEATHER_STATUSES = {
    'Rain': r'Rainy ☔☔☔',
    'Clear': r'Sunny ☀️☀️☀️',
    'Clouds': r'Clody ☁️☁️☁️',
    'Wind': r'Windy 🌪️🌪️🌪️',
    'Drizzle': r'Just a little drizzle 🌧️🌧️🌧️',
    'Thunderstorm': r'Thunder, be careful 🌩️🌩️🌩️',
    'Snow': r'Snowy ❄️❄️❄️',
    'Mist': r'Misty 🌫️🌫️🌫️'
}

bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(
        'Hello, my friend!\nText me the name of the '
        'city you want to know about'
    )


@dispatcher.message_handler()
async def get_current_weather(message: types.Message):
    """Получаем данные с сайта"""
    try:
        request = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}'
            f'&appid={WEATHER_TOKEN}&units=metric'
        )
        response = request.json()

        weather_description = response["weather"][0]["main"]
        if weather_description in WEATHER_STATUSES:
            wd = WEATHER_STATUSES[weather_description]
        else:
            wd = 'Strange Weather'

        city = response["name"]
        temperature = int((response["main"]["temp"]))
        humidity = response["main"]["humidity"]
        wind = response["wind"]["speed"]
        sunrise = dt.datetime.fromtimestamp(response["sys"]["sunrise"])
        sunset = dt.datetime.fromtimestamp(response["sys"]["sunset"])

        await message.reply(
            f"***{dt.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f"In {city}\nTemperature is {temperature}°C\n{wd}\n"
            f"Humidity: {humidity}%\nWind: {wind} m/s\nSunrise: {sunrise}\n"
            f"Sunset: {sunset}\nTime of sunrise and sunset depends "
            "on your timesunset depends on your time"
        )
    except Exception:
        await message.reply('😯 You need to check the name of city 😯')


if __name__ == '__main__':
    executor.start_polling(dispatcher)
