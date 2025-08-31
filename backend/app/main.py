from fastapi import FastAPI

from .routes import profile

app = FastAPI(title="Predusk Assessment API")

app.include_router(profile.router, prefix="")


@app.get("/")
async def root():
    return {"message": "Welcome to the Predusk Assessment API"}


@app.get("/health")
async def health():
    return {"status": "ok"}
