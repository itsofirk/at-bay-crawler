import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider


class ScrapySpider(CrawlSpider):
    name = "web_crawler"
    handle_httpstatus_list = [404, 500]  # Handle 404 and 500 errors

    def __init__(self, crawl_task=None, *args, **kwargs):
        super(ScrapySpider, self).__init__(*args, **kwargs)
        self.start_urls = [crawl_task['url']]
        self.allowed_domains = [crawl_task['allowed_domains']]
        self.rules = (
            Rule(LinkExtractor(allow_domains=self.allowed_domains), callback='parse_item', follow=True),
        )

    def parse_item(self, response):
        if response.status in self.handle_httpstatus_list:
            raise CloseSpider('Response code {} for url {}'.format(response.status, response.url))

        page_html = response.text
        # Here you can add the logic to store the HTML in your desired location
        # For example, you can store it in a file or a database
        # In this example, we'll just print it
        print(page_html)
