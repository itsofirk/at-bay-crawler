from scrapy.crawler import CrawlerProcess
from crawler.scrapy_spider import ScrapySpider
from infra.base_storage import BaseStorage
from infra.db import set_status
from infra.queue import queue
from common.enums import CrawlStatus
from multiprocessing import Pool


class CrawlManager:
    def __init__(self, feed_storage: BaseStorage, max_parallel_jobs: int = 1):
        self.max_parallel_jobs = max_parallel_jobs
        self.pool = Pool(processes=max_parallel_jobs)  # Create a pool of worker processes
        self.feed_storage = feed_storage

    def start_listening(self):
        while True:
            crawl_request = queue.get()  # Get the crawl request from the queue
            # Process the crawl request asynchronously
            self.pool.apply_async(self.process_crawl_request, (crawl_request,))

    def process_crawl_request(self, crawl_request):
        crawl_id = crawl_request['crawl_id']
        set_status(crawl_id, CrawlStatus.RUNNING.value)
        self._start_scrapy_crawler(crawl_id, crawl_request)
        set_status(crawl_id, CrawlStatus.COMPLETE.value)

    def _start_scrapy_crawler(self, job_id, crawl_requests):
        process = CrawlerProcess(settings={
            'FEEDS': {
                'items.json': {'format': 'json'},
            },
        })
        for crawl_request in crawl_requests:
            process.crawl(ScrapySpider, feed_storage=self.feed_storage, crawl_request=crawl_request)
        process.start()
