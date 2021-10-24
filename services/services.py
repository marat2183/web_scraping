import requests
from bs4 import BeautifulSoup
import re
from parsers.parsers import FilmsParser, FilmParser, WorkersParser
from handlers.handlers import FilmsHtmlHandler, FilmHtmlHandler, WorkersHtmlHandler


class FilmsService():
    def __init__(self, url: str, params=None, headers=None, proxies=None):
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        if proxies is None:
            proxies = {}
        self.parser = FilmsParser(url=url, params=params, headers=headers, )
        self.serializer = FilmsHtmlHandler()


class FilmService():
    def __init__(self, url, params=None, headers=None, proxies=None):
        print("Hello")
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        if proxies is None:
            proxies = {}
        self.parser = FilmParser(url=url, params=params, headers=headers, proxies=proxies)
        self.serializer = FilmHtmlHandler()


class WorkersService():
    def __init__(self, url, params=None, headers=None):
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        self.parser = WorkersParser(url=url, params=params, headers=headers)
        self.serializer = WorkersHtmlHandler()