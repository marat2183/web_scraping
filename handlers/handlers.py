import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
from typing import Union


class Film():
    def __init__(self, image_link, film_url, film_id, name, date, country, genres, rating, status=True):
        self.image_link = image_link
        self.film_url = film_url
        self.film_id = film_id
        self.name = name
        self.date = date
        self.country = country
        self.genres = genres
        self.rating = rating
        self.status = status

    @staticmethod
    def get_films_ids(films):
        ids = map(lambda film: film.id, films)
        return ids


class FilmsHtmlHandler():
    @staticmethod
    def _get_film_img_link(film: BeautifulSoup) -> str:
        img_link = film.find('img', class_="selection-film-item-poster__image").get('src')
        if img_link:
            return "https:" + img_link
        else:
            error = "Не удалось получисть картинку"
            return error

    @staticmethod
    def _get_film_link(film: BeautifulSoup) -> str:
        link = film.find("a", class_="selection-film-item-meta__link").get('href')
        if link:
            return "https://www.kinopoisk.ru/" + link
        else:
            error = "Не удалось получить ссылку"
            return error

    @staticmethod
    def _get_film_id(film: BeautifulSoup) -> Union[str, int]:
        film_id = film.find("a", class_="selection-film-item-meta__link").get('href').split('/')[2]
        if film_id:
            return int(film_id)
        else:
            error = "Не удалось получить номер фильма"
            return error

    @staticmethod
    def _get_film_name(film: BeautifulSoup) -> str:
        name = film.find('p', class_='selection-film-item-meta__name').text
        if name:
            return name
        else:
            error = "Не удалось получить название фильма"
            return error

    @staticmethod
    def _get_film_date(film: BeautifulSoup) -> str:
        date = film.find('p', class_='selection-film-item-meta__original-name').text.split(',')[-1].strip()
        if date:
            return date
        else:
            error = "Не удалось получить дату выхода сериала"
            return error

    @staticmethod
    def _get_film_country(film: BeautifulSoup) -> str:
        country = film.find('p', class_="selection-film-item-meta__meta-additional").findChildren(recursive=False)[
            0].text
        if country:
            return country
        else:
            error = "Не удалось получить страну сериала"
            return error

    @staticmethod
    def _get_film_genre(film: BeautifulSoup) -> str:
        genre = film.find('p', class_="selection-film-item-meta__meta-additional").findChildren(recursive=False)[1].text
        if genre:
            return genre
        else:
            error = "Не удалось получить жанр сериала"
            return error

    @staticmethod
    def _get_film_rating(film: BeautifulSoup) -> str:
        rating = film.find('span', class_="rating__value").text
        if rating:
            return rating
        else:
            error = "Не удалось получить рейтинг сериала"
            return error

    def _to_dict(self, **kwargs) -> dict:
        res_dict = {}
        timestamp = int(time.mktime(datetime.now().timetuple()))
        for key, value in kwargs.items():
            res_dict[key] = value
            res_dict['timestamp'] = timestamp
        return res_dict

    def get_films(self, data: list) -> list:
        films_objs = []
        films = data
        for film in films:
            img_link = self._get_film_img_link(film)
            link = self._get_film_link(film)
            film_id = self._get_film_id(film)
            name = self._get_film_name(film)
            date = self._get_film_date(film)
            country = self._get_film_country(film)
            genre = self._get_film_genre(film)
            rating = self._get_film_rating(film)
            film_obj = self._to_dict(name=name, film_url=link, film_id=film_id, image_link=img_link, date=date,
                              country=country,
                            genres=genre, rating=rating)
            films_objs.append(film_obj)
        return films_objs


class FilmHtmlHandler():
    dont_parse = ["Режиссер", "Продюсер", "Сценарий", "Оператор", "Композитор", "Художник", "Монтаж", "Бюджет",
                  "Сборы в США", "Сборы в мире"]

    def loads_html(self, data, film_id):
        serial_data = {}
        categories = data["msg"]
        for cat in categories:
            cat_name = cat.findChildren(recursive=False)[0].text
            cat_value = cat.findChildren(recursive=False)[1].text
            if cat_name in self.dont_parse:
                continue
            else:
                if ", ..." in cat_value:
                    cat_value = cat_value.replace(", ...", "")
                if cat_name == "Жанр":
                    cat_value = cat_value[:-5]
            serial_data[cat_name] = cat_value
        serial_data["film_id"] = film_id
        return serial_data


class WorkersHtmlHandler():
    @staticmethod
    def _get_types_of_dif_workers(page_html_data):
        types_list_html = page_html_data.find('td', class_="anchers").find_all('a', class_="all")
        type_workers = list(map(lambda x: x.text, types_list_html))
        return type_workers

    @staticmethod
    def _get_nums_of_dif_workers(page_html_data):
        workers = list(map(lambda item: item.text, page_html_data.find_all('div', class_="num")))
        temp = workers.count("1.")
        res = []
        r = 0
        for i in range(temp):
            new_ind = workers.index('1.')
            workers[new_ind] = False
            if i == 0:
                r = new_ind
                continue
            res.append((r, (new_ind - r)))
            r = new_ind
        res.append((r, (len(workers) - r)))
        return res

    def workers_num_and_type_info(self, page_html_data):
        type_worker = self._get_types_of_dif_workers(page_html_data[0])
        res = self._get_nums_of_dif_workers(page_html_data[0])
        res_dict = {}
        for i in range(len(type_worker)):
            res_dict[type_worker[i]] = res[i]
        return res_dict

    def _get_res(self, prof: str, indxs: tuple, workers_data, film_id):
        temp_list = []
        workers_data = workers_data[1]
        start_ind, number = indxs
        end_ind = number if number <= 5 else 5
        for i in range(start_ind, start_ind + end_ind):
            worker_dict = {}
            worker = workers_data[i]
            worker_name = worker.find('div', class_="name").find('a').text
            worker_img_link = worker.find('div', class_="photo").find('img', class_="flap_img").get('title')
            worker_dict["Профессия"] = prof
            worker_dict["Имя"] = worker_name
            worker_dict["Картинка"]= "https://www.kinopoisk.ru/" + worker_img_link
            worker_dict["Фильм"] = film_id
            temp_list.append(worker_dict)
        return temp_list

    def load_html(self, workers_data, film_id):
        res_list = []
        r = self.workers_num_and_type_info(workers_data)
        for k, v in r.items():
            workers = self._get_res(k, v, workers_data, film_id)
            res_list += workers
        return res_list