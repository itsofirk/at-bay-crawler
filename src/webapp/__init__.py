from fastapi import FastAPI

from common.logging_utils import setup_logger

app = FastAPI()
setup_logger(__name__)
