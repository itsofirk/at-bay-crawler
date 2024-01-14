from fastapi import HTTPException

from app import app as fastapi_app
from app.models import CrawlRequest
from crawler.spider import Spider


@fastapi_app.post('/crawl')
def initiate_crawl(crawl_request: CrawlRequest):
    try:
        crawl_id = Spider.initiate_crawl(crawl_request)
        return {'crawl_id': crawl_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Invalid request data: {str(e)}')

# Endpoint to check the status of a crawl
@fastapi_app.get('/status/{crawl_id}')
def get_crawl_status(crawl_id: str):
    status = Spider.get_crawl_status(crawl_id)
    if status:
        return {'status': status}
    else:
        raise HTTPException(status_code=404, detail='Crawl-id not found')
