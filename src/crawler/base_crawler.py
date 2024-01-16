import logging
from typing import List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from crawler.rules import BaseRule

logger = logging.getLogger(__name__)


class BaseCrawler:
    def __init__(self, start_url, crawl_id, rules: List[BaseRule] = None):
        self.start_url = start_url
        self.crawl_id = crawl_id
        self.rules = rules or []
        self.visited_urls = set()

    def crawl(self):
        logger.info(f'Starting crawl for {self.crawl_id}')
        self.process_url(self.start_url)
        self.visited_urls.add(self.start_url)

    def process_url(self, url):
        """
        Process a single URL and return.
        """
        raise NotImplementedError("Subclasses must implement the process_url method")

    def check_rules(self, url):
        """
        Check if the url matches all the rules in the rules list
        """
        return all(rule.check(url) for rule in self.rules)

    def check_visited(self, url):
        return url in self.visited_urls

    def extract_links(self, response):
        """
        Extract follow-up links from the html that match the rules
        """
        html = response.text
        try:
            soup = BeautifulSoup(html, 'html.parser')
        except Exception as e:
            logger.error(f"Error parsing HTML: {str(e)}")
            return
        for a in soup.find_all('a', href=True):
            link = a.get('href')
            parsed_url = urlparse(link)
            if not parsed_url.netloc:
                link = urljoin(self.start_url, link)
            if not self.check_visited(link) and self.check_rules(link):
                yield link
