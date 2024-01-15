import logging
import uvicorn
from multiprocessing import Process
from crawler.crawl_manager import CrawlManager
from infra.local_fs_storage import LocalFSStorage

logger = logging.getLogger(__name__)


def start_webapp():
    try:
        uvicorn.run("webapp.views:app", host="0.0.0.0", port=8000)
        logger.info('Webapp started successfully.')
    except Exception as e:
        logger.error(f'Error starting webapp: {str(e)}')


if __name__ == "__main__":
    try:
        # Create the feed storage
        feed_storage = LocalFSStorage(base_dir="crawl_jobs")

        # Create the webapp process
        webapp_process = Process(target=start_webapp)
        webapp_process.start()

        # Create the crawler process
        crawl_manager = CrawlManager(feed_storage=feed_storage)
        crawler_process = Process(target=crawl_manager.start_listening)
        crawler_process.start()

        # Wait for the processes to finish
        webapp_process.join()
        crawler_process.join()
    except Exception as e:
        logger.error(f'Error in main process: {str(e)}')
