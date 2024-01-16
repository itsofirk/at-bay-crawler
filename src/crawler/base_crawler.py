from typing import List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from crawler.rules import BaseRule
from infra.base_storage import BaseStorage


class BaseCrawler:
    def __init__(self, feed_storage: BaseStorage, crawl_id, rules: List[BaseRule] = None):
        self.feed_storage = feed_storage
        self.crawl_id = crawl_id
        self.rules = rules or []

    def crawl(self, url, depth):
        raise NotImplementedError("Subclasses must implement the crawl method")

    def check_rules(self, url):
        """
        Check if the url matches all the rules in the rules list
        """
        return all(rule.check(url) for rule in self.rules)

    def extract_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a', href=True):
            link = a.get('href')
            parsed_url = urlparse(link)
            if not parsed_url.netloc:
                link = urljoin(self.start_url, link)
            if self.check_rules(link):
                yield link
