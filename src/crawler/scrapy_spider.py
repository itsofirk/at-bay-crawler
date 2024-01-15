from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

# Assuming the object_storage module is in infra/object_storage.py
from infra.object_storage import save_html


class ScrapySpider(CrawlSpider):
    name = "web_crawler"
    handle_httpstatus_list = [404, 500]  # Handle 404 and 500 errors

    def __init__(self, crawl_task=None, *args, **kwargs):
        super(ScrapySpider, self).__init__(*args, **kwargs)
        self.start_urls = [crawl_task['url']]
        self.allowed_domains = [crawl_task['allowed_domains']]
        self.crawl_id = crawl_task['crawl_id']
        self.rules = (
            Rule(LinkExtractor(allow_domains=self.allowed_domains), callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        if response.status in self.handle_httpstatus_list:
            raise CloseSpider('Response code {} for url {}'.format(response.status, response.url))

        page_html = response.text
        save_html(self.crawl_id, page_html)
