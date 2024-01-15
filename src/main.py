import uvicorn
from multiprocessing import Process
from crawler.crawl_manager import CrawlManager
from infra.local_fs_storage import LocalFSStorage


def start_webapp():
    uvicorn.run("webapp.views:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
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
