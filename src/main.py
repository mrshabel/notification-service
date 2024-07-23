from fastapi import FastAPI
from src.config import settings
from src.routers import (
    health_check
)

app = FastAPI(title=settings.APP_NAME, summary=settings.APP_DESCRIPTION)

# include routers
app.include_router(router=health_check.router, tags=["Health Check Endpoint"])
