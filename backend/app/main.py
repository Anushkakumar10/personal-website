from fastapi import FastAPI

from .routes import routers

app = FastAPI(title="Backend API")

# register all routers exported by the routes package
for r in routers:
    app.include_router(r, prefix="")


@app.get("/")
async def root():
    return {"message": "Welcome to the Backend API"}


@app.get("/health")
async def health():
    return {"status": "ok"}
