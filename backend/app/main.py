from fastapi import FastAPI

from .routes import routers
from .logger import logger

app = FastAPI(title="Backend API")

# register all routers exported by the routes package
for r in routers:
    app.include_router(r, prefix="/api")


@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to the Backend API"}


@app.get("/health")
async def health():
    logger.debug("Health check requested")
    return {"status": "ok"}
