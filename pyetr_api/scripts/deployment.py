from fastapi import FastAPI
from starlette.responses import PlainTextResponse
from pyetr_api import get_pyetr_router
import argparse

import multiprocessing

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gunicorn.app.base import BaseApplication

def get_app():
    app = FastAPI(default_response_class=PlainTextResponse, root_path='/pyetr_api')
    get_pyetr_router(app)


    origins = [
        "https://client.dreamingspires.dev/",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        if self.cfg is not None:
            config = {
                key: value
                for key, value in self.options.items()
                if key in self.cfg.settings and value is not None
            }
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def run():
    parser = argparse.ArgumentParser(
        prog="Pyetr API",
        description="What the program does",
        epilog="Text at the bottom of help",
    )
    parser.add_argument("-b", "--bind")
    out = parser.parse_args()

    options = {
        "bind": out.bind,
        "workers": (multiprocessing.cpu_count() * 2) + 1,
        "reload": True,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
    app = get_app()
    StandaloneApplication(app, options).run()
