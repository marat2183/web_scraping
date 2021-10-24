from parsers.parsers import FilmsParser
from handlers.handlers import FilmsHtmlHandler


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