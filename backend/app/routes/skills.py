from fastapi import APIRouter, Query

router = APIRouter()

_skills = ["python", "fastapi", "sqlalchemy", "javascript"]


@router.get("/skills/top")
async def top_skills(limit: int = 10):
    return _skills[:limit]


@router.get("/skills/search")
async def search_skills(q: str = Query(...)):
    return [s for s in _skills if q.lower() in s.lower()]
