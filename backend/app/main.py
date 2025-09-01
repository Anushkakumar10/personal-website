import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from fastapi import FastAPI

from app.routes import routers
from app.logger import logger

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
