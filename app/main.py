from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import init_db

from .routers import pages
from .routers import auth
from .routers import planners
from .routers import history


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


app.include_router(
    pages.router
)

app.include_router(
    auth.router
)

app.include_router(
    planners.router
)

app.include_router(
    history.router
)


@app.get("/startup")
def startup():

    return {
        "status": "ready",
        "gemini_enabled": bool(
            settings.gemini_api_key
        )
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )