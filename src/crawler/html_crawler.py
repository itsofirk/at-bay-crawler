import requests
from common.enums import CrawlStatus
from crawler.base_crawler import BaseCrawler
from infra.base_storage import BaseStorage


class HTMLCrawler(BaseCrawler):
    def __init__(self, start_url, crawl_id, feed_storage: BaseStorage, rules):
        super(HTMLCrawler, self).__init__(start_url, crawl_id, rules=rules)
        self.feed_storage = feed_storage

    def crawl(self):
        self.feed_storage.save_crawl_request(self.crawl_id, self.start_url)
        super().crawl()

    def process_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            page_html = response.text
            self.feed_storage.save_html(self.crawl_id, url, page_html)

            links = self.extract_links(response)
            valid_links = [link for link in links if all(rule.check(link) for rule in self.rules)]

            for link in valid_links:
                self.process_url(link)

            return CrawlStatus.COMPLETE
        except requests.exceptions.RequestException as e:
            print(f"Error crawling {url}: {str(e)}")
            return CrawlStatus.ERROR
