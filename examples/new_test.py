from fastapi import FastAPI
from starlette.responses import PlainTextResponse
from pyetr_api import get_pyetr_router
import uvicorn

if __name__ == "__main__":
    app = FastAPI(default_response_class=PlainTextResponse)
    get_pyetr_router(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)