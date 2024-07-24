from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.config import settings
from src.models.database import database
from src.routers import (
    health_check
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect db before application starts
    await database.connect()
    yield
    # disconnect db after shutdown
    await database.disconnect()

app = FastAPI(title=settings.APP_NAME, summary=settings.APP_DESCRIPTION, lifespan=lifespan)

# include routers
app.include_router(router=health_check.router, tags=["Health Check Endpoint"])
