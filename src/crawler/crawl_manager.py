import logging
from multiprocessing import Pool

from crawler.crawl_job import CrawlJob
from infra.base_storage import BaseStorage

logger = logging.getLogger(__name__)


class CrawlManager:
    def __init__(self, feed_storage: BaseStorage, queue, max_parallel_jobs: int = 1):
        self.max_parallel_jobs = max_parallel_jobs
        self.feed_storage = feed_storage
        self.queue = queue
        logger.info('Crawl manager initialized successfully.')

    def start_listening(self):
        with Pool(processes=self.max_parallel_jobs) as pool:
            while True:
                logger.info('Waiting for new crawl request...')
                crawl_request = self.queue.get()
                logger.info(f'Received crawl request: {crawl_request}')
                try:
                    job = CrawlJob(self.feed_storage, crawl_request)
                    # Process the crawl request asynchronously
                    pool.apply(job.process_crawl_request)
                    logger.info(f'Crawl request added to processing queue. crawl_id: {crawl_request["crawl_id"]}')
                except Exception as e:
                    logger.error(f'Error processing crawl request: {str(e)}')