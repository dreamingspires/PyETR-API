from fastapi import FastAPI
from starlette.responses import PlainTextResponse
from pyetr_api import get_pyetr_router
import uvicorn


app = FastAPI(default_response_class=PlainTextResponse)
get_pyetr_router(app)
