import requests
from typing import List
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from infra.base_storage import BaseStorage
from common.enums import CrawlStatus


class SimpleCrawler:

    def __init__(self, feed_storage: BaseStorage, crawl_id: int, rules: List[str] = None):
        self.feed_storage = feed_storage
        self.crawl_id = crawl_id
        self.rules = rules or []

    def crawl(self, url, depth=2):
        try:
            response = requests.get(url)
            response.raise_for_status()

            page_html = response.text
            self.feed_storage.save_html(self.crawl_id, url, page_html)

            links = self.extract_links(page_html)
            valid_links = [link for link in links if all(rule.check(link) for rule in self.rules)]

            if depth > 1:
                for link in valid_links:
                    self.crawl(link, depth=depth - 1)

            return CrawlStatus.COMPLETE
        except requests.exceptions.RequestException as e:
            print(f"Error crawling {url}: {str(e)}")
            return CrawlStatus.ERROR

    def extract_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        absolute_links = [urljoin(self.start_url, link) for link in links]
        return absolute_links
