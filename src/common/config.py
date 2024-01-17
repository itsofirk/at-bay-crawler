from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Database Configuration
    DB_HOST: str = 'your_db_host'
    DB_PORT: int = 6379  # Replace with your actual port
    DB_PASSWORD: str = 'your_db_password'
    DB_DB: int = 0  # Replace with your actual database number

    # Web Crawler Configuration
    CRAWLER_MAX_PARALLEL_JOBS: int = 1  # Adjust as needed

    # Web App Configuration
    WEBAPP_HOST: str = '0.0.0.0'
    WEBAPP_PORT: int = 8000

    # Feed Storage Configuration
    BASE_DIR: str = 'crawl_jobs'  # Replace with your actual base directory

    # Redis Configuration (used in infra/db.py)
    REDIS_CONFIG: dict = {
        'host': DB_HOST,
        'port': DB_PORT,
        'password': DB_PASSWORD,
        'db': DB_DB,
    }
