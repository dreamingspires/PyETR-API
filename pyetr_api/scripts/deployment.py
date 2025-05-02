from fastapi import FastAPI
from starlette.responses import PlainTextResponse
from pyetr_api import get_pyetr_router
import uvicorn

app = FastAPI(default_response_class=PlainTextResponse)
get_pyetr_router(app)

def run():
    uvicorn.run("pyetr_api.scripts.deployment:app", host="0.0.0.0", port=8000, reload=True, workers=4)