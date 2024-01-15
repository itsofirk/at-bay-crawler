import uuid
from fastapi import HTTPException

from webapp import app
from webapp.models import CrawlRequest
from common.db import set_status, get_status
from common.queue import queue


@app.post('/crawl')
def initiate_crawl(crawl_request: CrawlRequest):
    try:
        crawl_id = str(uuid.uuid4())  # Generate a unique crawl_id
        set_status(crawl_id, 'Accepted')
        crawl_request_dict = crawl_request.dict()
        crawl_request_dict['crawl_id'] = crawl_id  # Add the crawl_id to the crawl request
        queue.put(crawl_request_dict)  # Put the crawl request in the queue
        return {'crawl_id': crawl_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Invalid request data: {str(e)}')


@app.get('/status/{crawl_id}')
def get_crawl_status(crawl_id: str):
    status = get_status(crawl_id)
    if status:
        return {'status': status}
    else:
        raise HTTPException(status_code=404, detail='Crawl-id not found')
