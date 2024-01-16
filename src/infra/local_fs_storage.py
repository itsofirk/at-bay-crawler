import os
import logging
from urllib.parse import urlparse
from infra.base_storage import BaseStorage

logger = logging.getLogger(__name__)


class LocalFSStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_dir = kwargs.get('base_dir', 'crawl_jobs')

    def save_html(self, crawl_id, url, html_content, encoding="utf-8"):
        # Generate a filename from the URL
        parsed_url = urlparse(url)
        filename = f"{parsed_url.netloc}{parsed_url.path}".replace('/', '_')

        # Save the HTML content to a file
        html_filepath = os.path.join(self.base_dir, crawl_id, f"{filename}.html")
        logger.debug(f'Saving HTML content to file: {html_filepath}')
        with open(html_filepath, 'w', encoding=encoding) as f:
            f.write(html_content)
        return html_filepath

    def save_crawl_request(self, crawl_id, start_url):
        # Create a directory for the crawl_id if it doesn't exist
        crawl_dir = os.path.join(self.base_dir, crawl_id)
        logger.debug(f'Creating directory for crawl_id: {crawl_id} at {crawl_dir}')
        os.makedirs(crawl_dir, exist_ok=True)
        return os.path.abspath(crawl_dir)
