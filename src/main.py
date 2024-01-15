from multiprocessing import Process
from crawler.crawl_manager import CrawlManager
import uvicorn


def start_webapp():
    uvicorn.run("webapp.app:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    # Create the webapp process
    webapp_process = Process(target=start_webapp)
    webapp_process.start()

    # Create the crawler process
    crawl_manager = CrawlManager()
    crawler_process = Process(target=crawl_manager.start_listening)
    crawler_process.start()

    # Wait for the processes to finish
    webapp_process.join()
    crawler_process.join()
