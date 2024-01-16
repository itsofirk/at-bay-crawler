from urllib.parse import urljoin
from bs4 import BeautifulSoup

from infra.base_storage import BaseStorage


class BaseCrawler:
    def __init__(self, feed_storage: BaseStorage, crawl_id, rules=None):
        self.feed_storage = feed_storage
        self.crawl_id = crawl_id
        self.rules = rules or []

    def crawl(self, url, depth):
        raise NotImplementedError("Subclasses must implement the crawl method")

    def extract_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        absolute_links = [urljoin(self.start_url, link) for link in links]
        return absolute_links
