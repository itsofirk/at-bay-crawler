from scrapy.crawler import CrawlerProcess
from crawler.scrapy_spider import ScrapySpider
from common.db import set_status
from common.queue import queue


class CrawlManager:
    def __init__(self, max_parallel_jobs: int = 5):
        self.max_parallel_jobs = max_parallel_jobs
        self.results = {}

    def start_listening(self):
        while True:
            crawl_request = queue.get()  # Get the crawl request from the queue
            self.process_crawl_request(crawl_request)

    def process_crawl_request(self, crawl_request):
        crawl_id = crawl_request['crawl_id']
        set_status(crawl_id, 'Running')
        self._start_scrapy_crawler(crawl_id, crawl_request)
        set_status(crawl_id, 'Complete')

    def _start_scrapy_crawler(self, job_id, crawl_requests):
        process = CrawlerProcess(settings={
            'FEEDS': {
                'items.json': {'format': 'json'},
            },
        })
        for crawl_request in crawl_requests:
            process.crawl(ScrapySpider, crawl_request=crawl_request)
        process.start()
