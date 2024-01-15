from fastapi import HTTPException

from webapp import app
from webapp.models import CrawlRequest
from crawler.crawl_manager import CrawlManager


@app.post('/crawl')
def initiate_crawl(crawl_request: CrawlRequest):
    try:
        crawl_id = CrawlManager.initiate_crawl(crawl_request)
        return {'crawl_id': crawl_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Invalid request data: {str(e)}')


@app.get('/status/{crawl_id}')
def get_crawl_status(crawl_id: str):
    status = CrawlManager.get_crawl_status(crawl_id)
    if status:
        return {'status': status}
    else:
        raise HTTPException(status_code=404, detail='Crawl-id not found')