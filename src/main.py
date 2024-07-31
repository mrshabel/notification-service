from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from src.config import settings
from src.models.database import database
from src.routers import health_check, email


@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect db before application starts
    await database.connect()
    yield
    # disconnect db after shutdown
    await database.disconnect()


app = FastAPI(
    title=settings.APP_NAME,
    summary=settings.APP_DESCRIPTION,
    lifespan=lifespan,
    root_path="/notifications",  # specify root_path to notify application that it's behind a proxy
)

# mount static files
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

# include routers
app.include_router(router=health_check.router, tags=["Health Check Endpoint"])
app.include_router(router=email.router, tags=["Email Endpoints"])
