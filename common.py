import requests
from bs4 import BeautifulSoup
import re
from parsers.parsers import FilmsParser, FilmParser, WorkersParser
from handlers.handlers import FilmsHtmlHandler, FilmHtmlHandler, WorkersHtmlHandler
from services.services import FilmsService, FilmService, WorkersService



a = FilmsService(url="https://www.kinopoisk.ru/popular/films/country-1/",
                params={"quick_filters": "serials", "tab": "all", "page": 1})
pages_nums = a.parser.get_page_nums()
print(pages_nums)
films_html = a.parser.get_films_from_page(page_num=1)
films = a.serializer.get_films(data=films_html["msg"])

for film in films:
    print("-------------------------------------------------------------------------------------")
    print(f"Картинка: {film.image_link}")
    print(f"Ссылка: {film.film_url}")
    print(f"ИД: {film.film_id}")
    print(f"Название: {film.name}")
    print(f"Дата: {film.date}")
    print(f"Страна: {film.country}")
    print(f"Жанр: {film.genres}")
    print(f"Рейтинг: {film.rating}")

t = films[0]

a = FilmService(url='https://www.kinopoisk.ru{t}')
cat = a.parser.get_film_from_page(t.film_id)
b = a.serializer.loads_html(cat)
print(b)

a = WorkersService(url='https://www.kinopoisk.ru{t}')
cat = a.parser.get_workers_from_page(t.film_id)
b = a.serializer.get_res(cat["msg"])
# print(b)