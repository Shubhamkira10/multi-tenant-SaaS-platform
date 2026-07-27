from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import Base, engine
from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Elemental Platform")

    yield

    logger.info("Stopping Elemental Platform")