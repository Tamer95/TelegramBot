import requests
import json
import configparser
import logging
import re
from extensions import APIException, CryptoConverter

import telebot
from telebot import types

config = configparser.ConfigParser()
config.read('config.ini')

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(config['TELEGRAM']['ACCESS_TOKEN'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "Привет! Я могу помочь тебе конвертировать валюты.\n"
        "Чтобы начать работу, введи команду в следующем формате:\n"
        "<имя валюты цену которой он хочет узнать> "
        "<имя валюты в которой надо узнать цену первой валюты> "
        "<количество первой валюты>.\n"
        "Чтобы увидеть список всех доступных валют, введи команду /values.\n"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:\n"
    for currency in CryptoConverter.get_available_currencies():
        text += f"{currency}\n"
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        base, quote, amount = message.text.split(' ')
        result = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка конвертации:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Непредвиденная ошибка:\n{e}")
    else:
        text = f"{amount} {base} = {result} {quote}"
        bot.reply_to(message, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)


# [TELEGRAM]
# ACCESS_TOKEN = ваш_токен