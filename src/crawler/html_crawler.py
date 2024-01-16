import requests
from common.enums import CrawlStatus
from crawler.base_crawler import BaseCrawler
from crawler.rules.domain_rule import DomainRule
from infra.base_storage import BaseStorage


class HTMLCrawler(BaseCrawler):
    def __init__(self, start_url, crawl_id, feed_storage: BaseStorage):
        super(HTMLCrawler, self).__init__(start_url, crawl_id)
        self.feed_storage = feed_storage
        self.rules = [
            DomainRule(self.start_url),
        ]

    def crawl(self):
        crawl_directory = self.feed_storage.save_crawl_request(self.crawl_id, self.start_url)
        result = super().crawl()
        result["directory"] = crawl_directory
        result["crawl_id"] = self.crawl_id
        return result

    def process_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            page_html = response.text
            self.feed_storage.save_html(self.crawl_id, url, page_html, encoding=response.encoding)
            self.visited_urls.add(url)
            links = self.extract_links(response)

            for link in links:
                response = self.process_url(link)
                if response["status"] == CrawlStatus.ERROR:
                    return response  # Stop crawling if an error occurs

            return {"status": CrawlStatus.COMPLETE}
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            return {"status": CrawlStatus.ERROR, "error": str(e)}
