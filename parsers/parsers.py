import requests
from bs4 import BeautifulSoup
import re


class Parser():
    def __init__(self, url, params=None, headers=None):
        self.url = url
        if params is None:
            self.params = {}
        else:
            self.params = params
        if headers is None:
            self.headers = {}
        else:
            self.headers = headers

    def get_page_data(self):
        response = requests.get(url=self.url, params=self.params, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup


class FilmsParser(Parser):
    def get_page_nums(self):
        soup = self.get_page_data()
        pages = soup.find('div', class_="paginator").find_all('a', class_="paginator__page-number")[-1].text
        return int(pages)

    def get_films_from_page(self, page_num):
        self.params["page"] = page_num
        html_data = self.get_page_data()
        films_html = html_data.find('div', class_="selection-list").find_all('div',
                                                                             class_="desktop-rating-selection-film-item")
        if films_html:
            return {"status": "success", "msg": films_html}
        else:
            error = "Не удалось получить список файлов"
            return {"status": "error", "msg": error}


class FilmParser(Parser):
    def get_film_from_page(self, film_id):
        self.url = f"https://www.kinopoisk.ru/series/{film_id}/"
        html_data = self.get_page_data()
        serial_div = html_data.find('div', {"data-test-id": "encyclopedic-table"})
        serial_data = serial_div.findChildren(recursive=False)
        if serial_data:
            return {"status": "success", "msg": serial_data}
        else:
            error = "Не удалось получить информацию о сериале"
            return {"status": "error", "msg": error}


class WorkersParser(Parser):
    def get_workers_from_page(self, film_id):
        self.url = f"https://www.kinopoisk.ru/film/{film_id}/cast/"
        html_data = self.get_page_data()
        workers_data = html_data.find_all('div', class_="actorInfo")
        if workers_data:
            return {"status": "success", "msg": (html_data, workers_data)}
        else:
            error = "Не удалось получить информацию о сериале"
            return {"status": "error", "msg": error}