import uuid
import logging
from fastapi import HTTPException

from webapp import app
from webapp.models import CrawlRequest
from infra.db import set_status, get_status
from common.enums import CrawlStatus

logger = logging.getLogger(__name__)


@app.post('/crawl')
def initiate_crawl(crawl_request: CrawlRequest):
    try:
        crawl_id = str(uuid.uuid4())  # Generate a unique crawl_id
        set_status(crawl_id, CrawlStatus.ACCEPTED.value)
        crawl_request_dict = crawl_request.model_dump()
        crawl_request_dict['crawl_id'] = crawl_id
        app.queue.put(crawl_request_dict)
        logger.info(f'Crawl initiated successfully. crawl_id: {crawl_id}')
        return {'crawl_id': crawl_id}
    except Exception as e:
        logger.error(f'Error initiating crawl: {str(e)}')
        raise HTTPException(status_code=400, detail=f'Invalid request data: {str(e)}')


@app.get('/status/{crawl_id}')
def get_crawl_status(crawl_id: str):
    status = get_status(crawl_id)
    if status:
        logger.info(f'Crawl status retrieved successfully. crawl_id: {crawl_id}, status: {status}')
        return {'status': status}
    else:
        logger.warning(f'Crawl status not found. crawl_id: {crawl_id}')
        raise HTTPException(status_code=404, detail=CrawlStatus.NOT_FOUND.value)
