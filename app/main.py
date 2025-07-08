from fastapi import FastAPI
from .api.v1.endpoints import router as v1_router
from .api.v2.endpoints import router as v2_router

def create_app() -> FastAPI:
    app = FastAPI(title="Email-Classifier API")
    app.include_router(v1_router)
    app.include_router(v2_router)
    return app

app = create_app()
