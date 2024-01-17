import uvicorn
from multiprocessing import Process

from common.logging_utils import setup_logger
from infra.local_fs_storage import LocalFSStorage
from infra.queue import init_queue
from crawler.crawl_manager import CrawlManager
from crawler.html_crawler import HTMLCrawler

logger = setup_logger(__name__)


def start_webapp(queue):
    from webapp.views import app
    try:
        app.queue = queue
        uvicorn.run(app, host="0.0.0.0", port=8000)
        logger.info('Webapp started successfully.')
    except Exception as e:
        logger.error(f'Error starting webapp: {str(e)}')
        raise e


def setup_crawler_manager():
    feed_storage = LocalFSStorage(base_dir="crawl_jobs")
    return CrawlManager(HTMLCrawler,
                        queue=shared_queue,
                        max_parallel_jobs=1,
                        feed_storage=feed_storage)


def use_dotenv(dotenv_path=None):
    from dotenv import load_dotenv
    logger.warning(f'Using .env file to set environment variables')
    logger.debug(f'dotenv_path: {dotenv_path}')
    load_dotenv(dotenv_path=dotenv_path)


if __name__ == "__main__":
    try:
        shared_queue = init_queue()
        crawl_manager = setup_crawler_manager()

        webapp_process = Process(target=start_webapp, args=(shared_queue,))
        webapp_process.start()

        crawler_process = Process(target=crawl_manager.start_listening)
        crawler_process.start()

        # Wait for the processes to finish
        webapp_process.join()
        crawler_process.join()
    except Exception as e:
        logger.error(f'Error in main process: {str(e)}')
