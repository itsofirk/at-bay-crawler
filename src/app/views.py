from flask import jsonify
from app import app


@app.post('/crawl')
def initiate_crawl():
    crawl_id = Crawler.initiate_crawl()
    return jsonify({'crawl_id': crawl_id})


@app.get('/status/<crawl_id>')
def get_crawl_status(crawl_id):
    status = Crawler.get_crawl_status(crawl_id)
    if status:
        return jsonify({'status': status})
    return jsonify({'error': 'Crawl-id not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
