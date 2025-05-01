from fastapi import FastAPI
from .string_transform import Mode
from .string_transform import string_to_view as sv
from .string_transform import view_to_string as vs

def get_pyetr_router(app: FastAPI, mode: Mode = Mode.simple):
    @app.post("/update/{view1}/{view2}")
    async def update(view1: str, view2: str):
        return vs(sv(view1,mode).update(sv(view2,mode)),mode)

    @app.post("/inquire/{view1}/{view2}")
    async def inquire(view1: str, view2: str):
        return vs(sv(view1,mode).inquire(sv(view2,mode)),mode)

    @app.post("/query/{view1}/{view2}")
    async def query(view1: str, view2: str):
        return vs(sv(view1,mode).query(sv(view2,mode)),mode)
    
    @app.post("/factor/{view1}/{view2}")
    async def factor(view1: str, view2: str):
        return vs(sv(view1,mode).factor(sv(view2,mode)),mode)

    @app.post("/product/{view1}/{view2}")
    async def product(view1: str, view2: str):
        return vs(sv(view1,mode).product(sv(view2,mode)),mode)

    @app.post("/sum/{view1}/{view2}")
    async def sum(view1: str, view2: str):
        return vs(sv(view1,mode).sum(sv(view2,mode)),mode)

    @app.post("/answer/{view1}/{view2}")
    async def answer(view1: str, view2: str):
        return vs(sv(view1,mode).answer(sv(view2,mode)),mode)

    @app.post("/negation/{view}")
    async def negation(view1: str):
        return vs(sv(view1,mode).negation(),mode)
    
    @app.post("/merge/{view1}/{view2}")
    async def merge(view1: str, view2: str):
        return vs(sv(view1,mode).merge(sv(view2,mode)),mode)

    @app.post("/division/{view1}/{view2}")
    async def division(view1: str, view2: str):
        return vs(sv(view1,mode).division(sv(view2,mode)),mode)

    @app.post("/depose/{view}")
    async def depose(view1: str):
        return vs(sv(view1,mode).depose(),mode)
    
    @app.post("/which/{view1}/{view2}")
    async def which(view1: str, view2: str):
        return vs(sv(view1,mode).which(sv(view2,mode)),mode)
    
    @app.post("/universal_product/{view1}/{view2}")
    async def universal_product(view1: str, view2: str):
        return vs(sv(view1,mode).universal_product(sv(view2,mode)),mode)

    @app.post("/atomic_answer/{view1}/{view2}")
    async def atomic_answer(view1: str, view2: str):
        return vs(sv(view1,mode).atomic_answer(sv(view2,mode)),mode)

    @app.post("/equilibrium_answer/{view1}/{view2}")
    async def equilibrium_answer(view1: str, view2: str):
        return vs(sv(view1,mode).equilibrium_answer(sv(view2,mode)),mode)

    @app.post("/existential_sum/{view1}/{view2}")
    async def existential_sum(view1: str, view2: str):
        return vs(sv(view1,mode).existential_sum(sv(view2,mode)),mode)

    return app
