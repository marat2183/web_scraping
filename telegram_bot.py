import telebot
import time
from datetime import datetime
from db.db import DataBase
import threading
from telebot import types
from random import randrange
import os
import requests
from dotenv import load_dotenv
from main import updater

load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
API_TOKEN = os.getenv("API_TOKEN")
DB_NAME = os.getenv("DB_NAME")
DB = DataBase(
    host=HOST,
    port=int(PORT),
    db_name=DB_NAME)

SUBS_IDS = []

COMMANDS_STR = f"*Доступные команды:*\n" \
               f"/help - список команды\n" \
               f"/subscribe - подписаться на обновления\n" \
               f"/unsubscribe - отписаться от обновлений\n"

bot = telebot.TeleBot(API_TOKEN)


def data_to_markdown(film: dict):
    film_markdown_data = f"*Название:* {film['name']}\n" \
                         f"*Жанр:* {film['genres']}\n" \
                         f"*Страна:* {film['country']}\n" \
                         f"*Дата:* {film['date']}\n" \
                         f"*Рейнтинг:* {film['rating']}\n" \
                         f"[Подробнее]({film['film_url']})\n"
    return film_markdown_data


def periodic():
    while True:
        print("Подписчики для рассылки:", SUBS_IDS)
        films = updater()
        if films:
            for id in SUBS_IDS:
                for film in films:
                    film_data = data_to_markdown(film)
                    bot.send_message(id, film_data, parse_mode="markdown")
            time.sleep(60)
        else:
            time.sleep(60)
            continue


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    random_serial = types.KeyboardButton(text="Случайный сериал")
    command_list = types.KeyboardButton(text="Команды")
    markup.add(random_serial, command_list)
    bot.send_message(message.chat.id, COMMANDS_STR, parse_mode="markdown", reply_markup=markup)


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    if message.chat.id not in SUBS_IDS:
        SUBS_IDS.append(message.chat.id)
        # print(SUBS_IDS)
        bot.send_message(message.chat.id, "Вы успешно подписались на обновления")
    else:
        bot.send_message(message.chat.id, "Вы уже подписались на обновления")


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    if message.chat.id in SUBS_IDS:
        SUBS_IDS.remove(message.chat.id)
        # print(SUBS_IDS)
        bot.send_message(message.chat.id, "Вы успешно отписались от обновлений", )
    else:
        bot.send_message(message.chat.id, "Вы не подписаны на обновления")


@bot.message_handler(commands=['serials'])
def start_message(message):
    films = DB.get_all("films")[:10]
    for film in films:
        film_data = data_to_markdown(film)
        bot.send_message(message.chat.id, film_data, parse_mode="markdown")


@bot.message_handler(content_types=['text'])
def text_input(message):
    if message.text == "Случайный сериал":
        ids_list = DB.get_all_ids("films")
        index = randrange(len(ids_list))
        film = DB.get_by_film_id("films", ids_list[index])
        film_markdown_data = data_to_markdown(film)
        bot.send_message(message.chat.id, film_markdown_data, parse_mode="markdown")
    elif message.text == "Команды":
        bot.send_message(message.chat.id, COMMANDS_STR, parse_mode="markdown")
    else:
        bot.send_message(message.chat.id, "Введите одну из команд бота.\nЧтобы получисть список команд, введите /help")


if __name__ == "__main__":
    try:
        t = threading.Thread(target=periodic)
        t.start()
        bot.polling()
    except requests.exceptions.ConnectionError:
        print("Проблемы с соединением")
