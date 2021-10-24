from bs4 import BeautifulSoup
import time
from datetime import datetime
from typing import Union


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