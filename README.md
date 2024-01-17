## Getting Started

1. **Installation:** Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
2. **Start a redis server:**

    ```bash
   docker run -d --name redis -p 6379:6379 redis
   ```

2. **Run the Application:**

    ```bash
    python main.py
    ```

   The web application will be accessible at http://localhost:8000 by default.

## Usage

1. **Initiate a Crawl:**

   Send a POST request to `http://localhost:8000/crawl` with a `start_url` link, You will receive a unique `crawl_id` in
   response.

2. **Check Crawl Status:**

   Use the endpoint `http://localhost:8000/status/{crawl_id}` to check the status of a crawl using the
   received `crawl_id`. The possible statuses are:

    - Accepted
    - Running
    - Error
    - Complete
    - Not-Found

3. **Retrieve HTML Content:**

   If the crawl is complete, you can retrieve the HTML content from the location provided in the response.

## Configuration

The project configuration is managed through the `config.py` file in the `common` package. You can customize database
credentials, file locations, and other settings in this file.

## Unit Tests

The project includes unit tests to ensure the correctness of the implemented functionalities. Run the tests using:

```
pip install nose
cd src
nosetests ..\tests\
```

## External Dependencies

* FastAPI: FastAPI framework for building APIs
* Scrapy: Scrapy framework for web crawling
* Redis: Redis for data storage
* Beautiful Soup: Beautiful Soup for HTML parsing
* Requests: Requests library for HTTP requests