import requests
from common.enums import CrawlStatus
from crawler.base_crawler import BaseCrawler


class HTMLCrawler(BaseCrawler):
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
