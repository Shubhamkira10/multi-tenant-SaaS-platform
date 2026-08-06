from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
from app.core.lifespan import lifespan
from app.platform.mail.routes import router as mail_router
from app.platform.dashboard.routes import router as dashboard_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(
    api_router,
    prefix="/api",
)

app.include_router(
    mail_router,
    prefix="/api",
)

app.include_router(
    dashboard_router,
    prefix="/api",
)