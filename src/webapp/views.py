import uuid
import logging
from fastapi import HTTPException

from webapp import app
from webapp.models import CrawlRequest
from infra import db
from common.enums import CrawlStatus

logger = logging.getLogger(__name__)


@app.post('/crawl')
def initiate_crawl(crawl_request: CrawlRequest):
    try:
        crawl_id = str(uuid.uuid4())  # Generate a unique crawl_id
        db.set_status(crawl_id, CrawlStatus.ACCEPTED, start_url=crawl_request.start_url)
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
    crawl = db.get_crawl(crawl_id)
    logger.info(f'Crawl status retrieved successfully. crawl_id: {crawl_id}, status: {crawl["status"]}')
    if crawl["status"] == CrawlStatus.COMPLETE.value:
        return {'status': crawl["status"], 'directory': crawl["directory"]}
    elif crawl["status"] == CrawlStatus.ERROR.value:
        return {'status': crawl["status"], 'error': crawl["error"]}
    return {'status': crawl["status"]}
