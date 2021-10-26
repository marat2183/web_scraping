import requests
from bs4 import BeautifulSoup


class Parser():
    def __init__(self, url, params=None, headers=None, proxies=None):
        self.url = url
        if params is None:
            self.params = {}
        else:
            self.params = params
        if headers is None:
            self.headers = {}
        else:
            self.headers = headers
        if proxies is None:
            self.proxies = {}
        else:
            self.proxies = proxies

    def get_page_data(self):
        response = requests.get(url=self.url, params=self.params, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup


class FilmsParser(Parser):
    def get_page_nums(self) -> dict:
        soup = self.get_page_data()
        pages = soup.find('div', class_="paginator").find_all('a', class_="paginator__page-number")[-1].text
        if pages:
            try:
                pages = int(pages)
            except ValueError:
                return {"status": "error", "msg": "Не удалось получить количество страниц"}
            # if pages > 2:
            #     pages = 2
            return {"status": "success", "msg": pages}
        else:
            return {"status": "error", "msg": "Не удалось получить количество страниц"}

    def get_films_from_page(self, page_num: int) -> dict:
        self.params["page"] = page_num
        html_data = self.get_page_data()
        films_html = html_data.find('div', class_="selection-list").find_all('div',
                                                                             class_="desktop-rating-selection-film-item")
        if films_html:
            return {"status": "success", "msg": films_html}
        else:
            error = "Не удалось получить список фильмов"
            return {"status": "error", "msg": error}
