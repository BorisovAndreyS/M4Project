import logging
from abc import ABC
from datetime import datetime
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from openai import base_url

logger = logging.getLogger(__name__)

class SiteParse(ABC):
    def __init__(self, url: str, articles_path: str = ''):
        self.base_url = url
        self.articles_path = articles_path

    def parse(self):
        raise NotImplementedError

    def _normalize_url(self, url: str = ''):
        return self.base_url + self.articles_path + url

class HabrParser(SiteParse):
    def __init__(self):
        super().__init__('https://habr.com/', 'ru/articles/')
        self.source = 'habr'

    def parse(self):
        response = requests.get(self.base_url + self.articles_path,
                                headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
        },
                                timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        container = soup.find('div', class_='tm-articles-list')
        if not container:
            logger.warning('Не найдена лента статей — возможно, изменилась вёрстка')
            return []

        articles = container.find_all('article')
        res = []
        for article in articles:
            summary = article.find('div', class_='article-formatted-body').text
            id = article.get('id')
            title = article.find('h2').a.span.text
            url = self.base_url + self.articles_path + id
            dt = datetime.fromisoformat(article.find('time').get('datetime'))
            res.append({
                'title': title,
                'url' : url,
                'source': self.source,
                'summary': summary,
                'published_at' : dt})
        return res

pprint(HabrParser().parse())

