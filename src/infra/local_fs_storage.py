import os
from urllib.parse import urlparse
from infra.base_storage import BaseStorage


class LocalFSStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_dir = kwargs.get('base_dir', 'crawl_jobs')

    def save_html(self, crawl_id, url, html_content):
        # Create a directory for the crawl_id if it doesn't exist
        crawl_dir = os.path.join(self.base_dir, crawl_id)
        os.makedirs(crawl_dir, exist_ok=True)

        # Generate a filename from the URL
        parsed_url = urlparse(url)
        filename = f"{parsed_url.netloc}{parsed_url.path}".replace('/', '_')

        # Save the HTML content to a file
        html_filepath = os.path.join(crawl_dir, f"{filename}.html")
        with open(html_filepath, 'w') as f:
            f.write(html_content)
        return html_filepath
