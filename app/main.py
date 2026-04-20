import logging

from fastapi import FastAPI

from app.config import settings
from app.routers import items

logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(items.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
