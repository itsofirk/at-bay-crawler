import logging
from urllib.parse import urlparse

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

from infra.base_storage import BaseStorage

logger = logging.getLogger(__name__)


class ScrapySpider(CrawlSpider):
    name = "web_crawler"
    handle_httpstatus_list = [404, 500]  # Handle 404 and 500 errors

    def __init__(self, feed_storage: BaseStorage, crawl_request, *args, **kwargs):
        super(ScrapySpider, self).__init__(*args, **kwargs)
        self.start_urls = [crawl_request['url']]
        self.allowed_domains = [self.extract_domain(crawl_request['url'])]
        self.crawl_id = crawl_request['crawl_id']
        self.rules = (
            Rule(LinkExtractor(allow_domains=self.allowed_domains), callback='parse_item', follow=True),
        )
        self.feed_storage = feed_storage
        logger.info(f'ScrapySpider initialized successfully. crawl_id: {self.crawl_id}')

    def extract_domain(self, url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain

    def parse_item(self, response):
        logger.debug(f'Parsing item: {response.url}')
        if response.status in self.handle_httpstatus_list:
            raise CloseSpider('Response code {} for url {}'.format(response.status, response.url))

        page_html = response.text
        self.feed_storage.save_html(self.crawl_id, response.url, page_html)
