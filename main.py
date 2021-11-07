from services.services import FilmsService
from db.db import DataBase
from time import sleep
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
API_TOKEN = os.getenv("API_TOKEN")
DB_NAME = os.getenv("DB_NAME")

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}

db = DataBase(host=HOST, port=int(PORT), db_name=DB_NAME)
app = FilmsService(url="https://www.kinopoisk.ru/popular/films/country-1/",
                   params={"quick_filters": "serials", "tab": "all", "page": 1},
                   headers=headers)


def add_new_films(all_films_list):
    films_id_from_site = list(map(lambda film: film["film_id"], all_films_list))
    films_ids_from_db = db.get_all_ids("films")
    need_to_add_ids = list(set(films_id_from_site) - set(films_ids_from_db))
    if need_to_add_ids:
        data_to_add = [film for film in all_films_list if film["film_id"] in need_to_add_ids]
        print(f"Количество новых сериалов: {len(data_to_add)}")
        pprint(data_to_add)
        resp = db.insert_many(collection="films", data=data_to_add)
        if resp["status"] == "success":
            print("Данные успешно обновлены")
            return data_to_add
        else:
            print("Произошла ошибка при обновлении")
            return []
    else:
        print("Ничего нового нет")
        return []


def get_all_films_data(max_page_num):
    all_films_list = []
    cur_page_num = 1
    while cur_page_num <= max_page_num:
        sleep(10)
        films_html_resp = app.parser.get_films_from_page(page_num=cur_page_num)
        if films_html_resp["status"] == "success":
            films = app.serializer.get_films(data=films_html_resp["msg"])
            all_films_list += films
            cur_page_num += 1
        else:
            print(films_html_resp["msg"])
            all_films_list = []
            break
    return all_films_list


def updater():
    print("Обновление данных")
    page_nums_resp = app.parser.get_page_nums()
    if page_nums_resp["status"] == "success":
        max_page_num = page_nums_resp["msg"]
        print("Количество страниц:", max_page_num)
        all_films_list = get_all_films_data(max_page_num)
        if all_films_list:
            films = add_new_films(all_films_list)
            if films:
                return films
            else:
                return []
        else:
            return []
    else:
        print(page_nums_resp["msg"])
        return []



# if __name__ == "__main__":
#     try:
#         updater()
#     except KeyboardInterrupt:
#         exit(0)
