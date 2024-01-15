from fastapi import FastAPI

from common.logging_utils import setup_logger

setup_logger(__name__)
app = FastAPI()
