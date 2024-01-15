from scrapy.crawler import CrawlerProcess
from crawler.scrapy_spider import ScrapySpider


class CrawlManager:
    def __init__(self, max_parallel_jobs: int = 5):
        self.max_parallel_jobs = max_parallel_jobs
        self.results = {}

    def initiate_crawl(self, crawl_requests):
        job_id = self._generate_job_id()
        self._start_scrapy_crawler(job_id, crawl_requests)
        return job_id

    def get_crawl_status(self, job_id):
        return self.results.get(job_id, "Not-Found")

    def _generate_job_id(self):
        # Implement your logic to generate a unique job id
        return "job_id_placeholder"

    def _start_scrapy_crawler(self, job_id, crawl_requests):
        process = CrawlerProcess(settings={
            'FEEDS': {
                'items.json': {'format': 'json'},
            },
        })
        for crawl_request in crawl_requests:
            process.crawl(ScrapySpider, crawl_request=crawl_request)
        process.start()
