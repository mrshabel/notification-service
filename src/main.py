from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from src.config import settings
from src.models.database import database
from src.routers import health_check, email
from src.events import (
    start_broker_connection,
    close_broker_connection,
)
from src.events.consumers.event_bus import NotificationEventBus


@asynccontextmanager
async def lifespan(app: FastAPI):
    event_bus = NotificationEventBus()

    # start event bus
    event_bus.start()

    # connect db before application starts
    await database.connect()
    # run primary connection for all producers on main thread
    start_broker_connection()

    # store event bus state throughout the application lifecycle
    app.state.event_bus = event_bus

    yield
    # gracefully shutdown event bus before main application
    if hasattr(app.state, "event_bus"):
        event_bus.stop()
        print(app.state.event_bus)

    # disconnect db after shutdown
    await database.disconnect()
    close_broker_connection()


app = FastAPI(
    title=settings.APP_NAME,
    summary=settings.APP_DESCRIPTION,
    lifespan=lifespan,
    root_path="/notifications",  # specify root_path to notify application since it's behind a proxy
)

# mount static files
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

# include routers
app.include_router(router=health_check.router, tags=["Health Check Endpoint"])
app.include_router(router=email.router, tags=["Email Endpoints"])
