from .router import get_pyetr_router
from fastapi import FastAPI
from starlette.responses import PlainTextResponse
from pyetr_api import get_pyetr_router

__version__ = '0.1.0'

app = FastAPI(default_response_class=PlainTextResponse)
get_pyetr_router(app)